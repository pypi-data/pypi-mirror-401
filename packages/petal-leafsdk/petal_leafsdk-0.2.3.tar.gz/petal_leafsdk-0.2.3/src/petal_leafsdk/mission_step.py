# petal_leafsdk/mission_step.py

import numpy as np
import time
import json
import traceback
import uuid
from typing import Dict, Any, List, Optional, Tuple, Union, Sequence, Literal, Type
from abc import ABC, abstractmethod
from dataclasses import dataclass

from pymavlink import mavutil
from pymavlink.dialects.v20 import droneleaf_mav_msgs as leafMAV

from petal_app_manager.proxies.redis import RedisProxy
from petal_app_manager.proxies.external import MavLinkExternalProxy

from petal_leafsdk.redis_helpers import setup_redis_subscriptions, unsetup_redis_subscriptions
from petal_leafsdk.mavlink_helpers import setup_mavlink_subscriptions, unsetup_mavlink_subscriptions
from petal_leafsdk.setpoint_memory import SetpointMemory
from leafsdk.core.mission.trajectory import WaypointTrajectory #, TrajectorySampler
from leafsdk import logger
from leafsdk.utils.logstyle import LogIcons
from leafsdk.core.mission.mission_plan_step import (
    Tuple3D, MissionPlanStep, _GotoBase, GotoGPSWaypoint, GotoLocalPosition,
    YawAbsolute, GotoRelative, YawRelative, Takeoff, Wait, Land
)
from enum import Enum, auto

class StepState(Enum):
    """Enum representing the state of a mission step."""
    IDLE = auto()
    RUNNING = auto()
    PAUSED = auto()
    PENDING_COMPLETION = auto()
    COMPLETED = auto()

class StepCompletionState(Enum):
    """Enum representing the completion state of a mission step."""
    NONE = auto()
    SUCCESS = auto()
    FAILED = auto()
    CANCELED = auto()

class MissionStepExecutor(ABC):
    def __init__(self, step: MissionPlanStep, setpointMemory: SetpointMemory, mission_id: Optional[str] = None, mavlink_proxy: MavLinkExternalProxy = None, redis_proxy: RedisProxy = None, fc_status_provider=None):
        # self.state = StepState() # Holds the current state of the step
        self.state: StepState = StepState.IDLE
        self.completion_state: StepCompletionState = StepCompletionState.NONE
        self.setpoint_offset = setpointMemory
        self.mission_id = mission_id
        self.step: MissionPlanStep = step
        self.output = True # Indicates the logical output of the step (mostly used for conditional steps)
        self.mavlink_proxy = mavlink_proxy
        self.redis_proxy = redis_proxy
        self.fc_status_provider = fc_status_provider  # Reference to FC status provider
        self.setup()

    def reset(self):
        """Reset the step state for re-execution."""
        self.state = StepState.IDLE

    # def first_exec(self) -> bool:
    #     """Returns True if this is the first execution of the step logic."""
    #     return self.state.exec_count == 0
    
    def description(self) -> str:
        """Returns a string description of the step for logging purposes."""
        return self.step.description()
    
    def is_pausable(self) -> bool:
        """Returns True if the step is pausable."""
        return self.step.is_pausable()

    def is_cancelable(self) -> bool:
        """Returns True if the step can be cancelled."""
        return self.step.is_cancelable()
    
    def is_running(self) -> bool:
        """Returns True if the step is currently running."""
        return self.state in [StepState.RUNNING, StepState.PAUSED]
    
    def log_info(self):
        """Log information about the step."""
        self.step.log_info()

    @abstractmethod
    def execute_step_logic(self):
        """Execute the logic for the mission step - this is called repeatedly until the step is completed."""
        pass

    def setup(self):
        """Setup any resources needed for the step prior to mission plan execution."""
        self.reset()

    def start(self):
        """Execute one time operations at the start of the step."""
        pass

    def terminate(self):
        """Execute one time operations at the end of the step."""
        pass

    def execute_step(self) -> Tuple[bool, bool]:
        # Check cancellation before executing
        if self.state == StepState.COMPLETED:
            logger.debug(f"{LogIcons.SUCCESS} Step already completed: {self.description()}")
        elif self.state == StepState.PENDING_COMPLETION:
            self.terminate()
            logger.info(f"{LogIcons.SUCCESS} Done: {self.description()} completed!. Completion state: {self.completion_state.name}")
            self.state = StepState.COMPLETED
        elif self.state == StepState.PAUSED:
            pass  # Do nothing if paused, no logging here to avoid spam
        elif self.state == StepState.IDLE: #self.first_exec():
            self.start()
            self.log_info()
            self.state = StepState.RUNNING
        else: # RUNNING
            self.execute_step_logic()
        return self.output, self.state == StepState.COMPLETED

    def pause(self) -> bool:
        """Pause the step if it is pausable."""
        if self.is_pausable():
            if self.state == StepState.RUNNING:
                self.state = StepState.PAUSED
                # self.stop_trajectory()
                # self.send_pause_to_FC() # Deprecated, handled by distributed state
                logger.info(f"{LogIcons.PAUSE} Step paused: {self.description()}")
                return True
            else:
                return False
                logger.warning(f"{LogIcons.WARNING} Step is not running, cannot pause: {self.description()}, state={self.state}")
        else:
            logger.warning(f"{LogIcons.WARNING} Step is not pausable: {self.description()}")
            return False

    def stop_trajectory(self):
        # self.redis_proxy.publish(
        #         channel="/traj_sys/clear_queue_and_abort_current_trajectory_ori",
        #         message=json.dumps({"payload": 1})  #TODO this number is used in FC as boolean not int, better to pass True or false
        #     )
        self.redis_proxy.publish(
                channel="/traj_sys/generate_stop_traj_on_xyz_plane_from_states_by_deceleration",
                message=json.dumps({"payload": getattr(self.step, 'average_deceleration', 0.5)})
            )
    
    # def send_resume_to_FC(self) -> None:
    #     pass

    # def send_pause_to_FC(self) -> None:
    #     pass


    def resume(self) -> bool:
        """Resume the step if it was paused."""
        if self.state == StepState.PAUSED:
            # self.send_resume_to_FC() # Deprecated
            logger.info(f"{LogIcons.RUN} Step resumed: {self.description()}")
            self.state = StepState.RUNNING
            return True
        # elif self.state == StepState.IDLE:
        #     self.send_resume_to_FC()
        #     logger.warning(f"{LogIcons.RUN} resume occured on unpausable step: {self.description()}. Setting state to IDLE and re-executing step.")
        #     self.execute_step()
        #     return True
        else:
            logger.warning(f"{LogIcons.WARNING} Step is not paused nor IDLE, cannot resume: {self.description()}")
            return False

    def cancel(self) -> bool:
        """Cancel the step."""
        self.state = StepState.PENDING_COMPLETION
        self.completion_state = StepCompletionState.CANCELED
        self.terminate()
        logger.info(f"{LogIcons.CANCEL} Step canceled: {self.description()}")
        return True



class _GotoExecutor(MissionStepExecutor):
    def __init__(self, step: MissionPlanStep, setpointMemory: SetpointMemory, mission_id: Optional[str] = None, mavlink_proxy: MavLinkExternalProxy = None, redis_proxy: RedisProxy = None, fc_status_provider=None):
        super().__init__(step=step, setpointMemory=setpointMemory, mission_id=mission_id, mavlink_proxy=mavlink_proxy, redis_proxy=redis_proxy, fc_status_provider=fc_status_provider)

        # ---- Internal state ----
        self.yaw_offset = 0.0  # Default yaw offset
        self.waypoint_offset = [0.0, 0.0, 0.0]  # Default position offset
        self.trajectory = None
        self.uuid_str = str(uuid.uuid4())
        self.queued_traj_ids: Dict[str, bool] = {}   # trajectories waiting for completion, value indicates if completed
        self.current_traj_segment: int = 0           # index of segment being processed

    def reset(self):
        super().reset()
        self.queued_traj_ids = {}
        self.current_traj_segment = 0
        self.uuid_str = str(uuid.uuid4())

    def _handle_notify_trajectory_completed(self, channel: str, message: str) -> None:
        """
        Handle notification messages for trajectory completion.
        This function is triggered asynchronously by the Redis subscriber.

        It parses the message, extracts the trajectory_id, and stores it
        in an internal queue or list for later processing. This function
        must not block.

        Parameters
        ----------
        channel : str
            The Redis channel from which the message was received.
        message : str
            The message content, expected to be a JSON string with trajectory details.
        """
        logger.info(f"{LogIcons.SUCCESS} Received notification on {channel}: {message}")

        try:
            command_data = json.loads(message)
            traj_id = command_data.get("trajectory_id")

            if traj_id:
                self.queued_traj_ids[traj_id] = True
                logger.info(f"{LogIcons.SUCCESS} Trajectory completed: {traj_id}")
            else:
                logger.warning(f"{LogIcons.WARNING} Received notification without trajectory_id: {message}")
        except Exception as e:
            logger.error(f"{LogIcons.ERROR} Error parsing completion notification: {e}")

    def start(self):
        setup_redis_subscriptions(pattern="/petal-leafsdk/notify_trajectory_completed", callback=self._handle_notify_trajectory_completed, redis_proxy=self.redis_proxy)
        try:
            # Log detailed setpoint info for debugging
            setpoint_age = time.time() - self.setpoint_offset.last_update_time
            logger.info(
                f"{LogIcons.INFO} {self.__class__.__name__} START - Setpoint offset: "
                f"pos={self.setpoint_offset.waypoint_offset}, yaw={self.setpoint_offset.yaw_offset:.2f}rad, "
                f"updates={self.setpoint_offset.update_counter}, age={setpoint_age:.2f}s"
            )
            logger.info(f"{LogIcons.INFO} Step waypoints: {self.step.waypoints}")

            # Compute trajectory once
            self.pos_traj_ids, self.pos_traj_json, self.yaw_traj_ids, self.yaw_traj_json = self._compute_trajectory(
                                                                                                self.step.waypoints,
                                                                                                self.step.yaws_deg,
                                                                                                self.step.speed,
                                                                                                self.step.yaw_speed,
                                                                                                home=self.setpoint_offset.waypoint_offset,
                                                                                                home_yaw=self.setpoint_offset.yaw_offset,
                                                                                                cartesian=self.step.cartesian,
                                                                                            )
            
        except Exception as e:
            logger.error(f"{LogIcons.ERROR} Error computing trajectory: {e}")
            logger.error(traceback.format_exc())
            raise e

    def execute_step_logic(self):
        """
        Execute mission step logic for sequential trajectory publishing.
        This function is designed to be called periodically (non-blocking).
        """
        total_segments = len(self.pos_traj_json)

        # If there are no uncompleted trajectories, publish next segment
        if all(list(self.queued_traj_ids.values())):
            if self.current_traj_segment < total_segments:
                self._publish_trajectory_segment(
                    idx=self.current_traj_segment,
                    pos_traj_seg=self.pos_traj_json[self.current_traj_segment],
                    yaw_traj_seg=self.yaw_traj_json[self.current_traj_segment],
                    pos_traj_id=self.pos_traj_ids[self.current_traj_segment],
                    yaw_traj_id=self.yaw_traj_ids[self.current_traj_segment],
                )
                self.current_traj_segment += 1
            else:
                self.state = StepState.PENDING_COMPLETION
                self.completion_state = StepCompletionState.SUCCESS

    def terminate(self):
        super().terminate()
        unsetup_redis_subscriptions(pattern="/petal-leafsdk/notify_trajectory_completed", redis_proxy=self.redis_proxy)

    def _compute_trajectory(    # TODO make all parameters either degree or radians
        self,
        waypoints: Sequence[Tuple[float, float, float]],
        yaws_deg: Sequence[float],
        speed: Sequence[float],
        yaw_speed: Union[Sequence[float], Literal["sync"]],
        home: Tuple[float, float, float],
        home_yaw: float,
        cartesian: bool,
        is_yaw_relative: Optional[bool] = False,
    ) ->  Tuple[List[str], List[Optional[str]], List[str], List[Optional[str]]]:
        """
        Compute the trajectory for the given waypoints and yaws.
        This function generates trajectory JSON files for each segment
        and returns their identifiers.
        
        Parameters
        ----------
        waypoints : Sequence[Tuple[float, float, float]]
            List of waypoints as (lat, lon, alt) or (x, y, z).
        yaws_deg : Sequence[float]
            List of yaw commands in degrees at each waypoint.
        speed : Sequence[float]
            List of speeds (m/s) for each segment.
        yaw_speed : Sequence[float] or str
            List of yaw speeds (deg/s) for each segment, or 'sync' to match position trajectory.
        home : Tuple[float, float, float]
            Home position reference (lat, lon, alt) or (x, y, z).
        home_yaw : float
            Home yaw reference in radians.
        cartesian : bool
            If True, waypoints are in Cartesian coordinates; if False, GPS coordinates.
        is_yaw_relative : bool
            If True, interpret yaws as relative changes; otherwise absolute.

        Returns
        -------
        pos_traj_ids : List[str]
            List of position trajectory segment identifiers.
        pos_traj_json : List[Optional[str]]
            List of position trajectory JSON strings (None if static).
        yaw_traj_ids : List[str]
            List of yaw trajectory segment identifiers.
        yaw_traj_json : List[Optional[str]]
            List of yaw trajectory JSON strings (None if static).
        """

        # Create trajectory json files for each segment based on the waypoints and yaws
        self.trajectory = WaypointTrajectory(
            waypoints=waypoints,
            yaws_deg=yaws_deg,
            speed=speed,
            yaw_speed=yaw_speed,
            home=home,
            home_yaw=home_yaw,
            cartesian=cartesian,
            is_yaw_relative=is_yaw_relative
        )
        
        pos_traj_ids, pos_traj_json = self.trajectory.build_pos_polynomial_trajectory_json(self.uuid_str)
        yaw_traj_ids, yaw_traj_json = self.trajectory.build_yaw_polynomial_trajectory_json(self.uuid_str)

        return pos_traj_ids, pos_traj_json, yaw_traj_ids, yaw_traj_json

    def _publish_trajectory_segment(
        self,
        idx: int,
        pos_traj_seg: str,
        yaw_traj_seg: str,
        pos_traj_id: str,
        yaw_traj_id: str,
    ) -> None:
        """
        Publish a single trajectory segment (position and/or yaw) to Redis.

        This function does not block or wait for completion. Completion is
        handled asynchronously via `_handle_notify_trajectory_completed`.

        Parameters
        ----------
        idx : int
            Segment index (0-based).
        pos_traj_seg : str or None
            JSON string for the position trajectory segment, or None if static.
        yaw_traj_seg : str or None
            JSON string for the yaw trajectory segment, or None if static.
        pos_traj_id : str or None
            Identifier for the position trajectory segment.
        yaw_traj_id : str or None
            Identifier for the yaw trajectory segment.
        """
        try:
            if self.redis_proxy is None:
                logger.warning(f"{LogIcons.WARNING} Redis proxy not available, skipping trajectory publication")
                return

            # Skip publishing if both are None
            if pos_traj_seg is None and yaw_traj_seg is None:
                logger.warning(
                    f"{LogIcons.WARNING} Both position and yaw trajectory segments are static, "
                    f"skipping publication for segment {idx+1}"
                )
                return

            # Publish position trajectory
            if pos_traj_seg is not None:
                self.redis_proxy.publish(
                    channel="/traj_sys/queue_traj_primitive_pos",
                    message=pos_traj_seg,
                )
                self.queued_traj_ids[pos_traj_id] = False
                logger.info(f"{LogIcons.SUCCESS} Position trajectory segment {idx+1} published to Redis successfully")

            # Publish yaw trajectory
            if yaw_traj_seg is not None:
                self.redis_proxy.publish(
                    channel="/traj_sys/queue_traj_primitive_ori",
                    message=yaw_traj_seg,
                )
                self.queued_traj_ids[yaw_traj_id] = False
                logger.info(f"{LogIcons.SUCCESS} Yaw trajectory segment {idx+1} published to Redis successfully")

        except Exception as e:
            logger.error(f"{LogIcons.ERROR} Error publishing trajectory segment {idx+1}: {e}")


class GotoGPSWaypointExecutor(_GotoExecutor):
    def __init__(self, step: GotoGPSWaypoint, setpointMemory: SetpointMemory, mission_id: Optional[str] = None, mavlink_proxy: MavLinkExternalProxy = None, redis_proxy: RedisProxy = None, fc_status_provider=None):
        super().__init__(step=step, setpointMemory=setpointMemory, mission_id=mission_id, mavlink_proxy=mavlink_proxy, redis_proxy=redis_proxy, fc_status_provider=fc_status_provider)
        self._converted_to_local = False
        self._local_waypoints = []
    
    def start(self):
        """Convert GPS waypoints to local positions using origin, then execute as local."""
        setup_redis_subscriptions(pattern="/petal-leafsdk/notify_trajectory_completed", callback=self._handle_notify_trajectory_completed, redis_proxy=self.redis_proxy)
        
        try:
            # Check if we have GPS origin available
            if not self.fc_status_provider or not self.fc_status_provider.has_gps_origin():
                raise RuntimeError(
                    "GPS waypoint execution requires GPS origin to be set. "
                    "Wait for GPS_GLOBAL_ORIGIN message or HOME_POSITION to calculate origin."
                )
            
            # Import coordinate conversion utilities
            from petal_leafsdk.coordinate_utils import GeoPoint, CoordinateConverter
            
            # Get GPS origin
            gps_origin_obj = self.fc_status_provider.get_gps_origin()
            origin_gps = gps_origin_obj.gps
            
            # Make source description clearer
            source_description = {
                "message": "GPS_GLOBAL_ORIGIN MAVLink message",
                "calculated": "calculated from HOME_POSITION",
                "unknown": "unknown source"
            }.get(gps_origin_obj.source, gps_origin_obj.source)
            
            logger.info(
                f"{LogIcons.SUCCESS} Converting {len(self.step.waypoints)} GPS waypoints to local NED using origin: "
                f"({origin_gps.lat_deg:.7f}, {origin_gps.lon_deg:.7f}, {origin_gps.alt_m:.2f}m) [source: {source_description}]"
            )
            
            # Convert GPS waypoints to local NED
            converter = CoordinateConverter(origin=origin_gps)
            self._local_waypoints = []
            
            # Get home position for validation and altitude conversion
            home_position = self.fc_status_provider.get_home_position()
            
            for idx, gps_wp in enumerate(self.step.waypoints):
                # GPS waypoint format: (lat_deg, lon_deg, alt_m)
                # NOTE: The altitude in the waypoint can be either:
                # 1. Absolute MSL altitude (if > 100m, likely MSL)
                # 2. Relative altitude above home (if < 100m, likely relative)
                # We detect this and convert relative to MSL if needed
                
                wp_alt_input = gps_wp[2]
                wp_lat = gps_wp[0]
                wp_lon = gps_wp[1]
                
                # Detect if altitude is relative or absolute MSL
                if home_position and home_position.is_set and home_position.gps:
                    home_alt_msl = home_position.gps.alt_m
                    
                    # If input altitude is much smaller than home altitude, it's likely relative
                    # Heuristic: if alt < 100m and home > 100m, treat as relative
                    if wp_alt_input < 100.0 and home_alt_msl > 100.0:
                        # Convert relative to MSL
                        wp_alt_msl = home_alt_msl + wp_alt_input
                        logger.info(
                            f"{LogIcons.INFO} WP{idx}: Detected relative altitude {wp_alt_input:.1f}m, "
                            f"converting to MSL: {wp_alt_msl:.1f}m (home at {home_alt_msl:.1f}m MSL)"
                        )
                    else:
                        # Treat as absolute MSL
                        wp_alt_msl = wp_alt_input
                        
                        # Warn if this results in waypoint far below home
                        alt_diff = wp_alt_msl - home_alt_msl
                        if alt_diff < -10.0:
                            logger.warning(
                                f"{LogIcons.WARNING} WP{idx} altitude ({wp_alt_msl:.1f}m MSL) is {abs(alt_diff):.1f}m below home ({home_alt_msl:.1f}m MSL). "
                                f"If you meant relative altitude, use values < 100m when home > 100m MSL."
                            )
                else:
                    # No home position, treat as absolute MSL
                    wp_alt_msl = wp_alt_input
                    logger.warning(f"{LogIcons.WARNING} No home position available, treating altitude as absolute MSL")
                
                # Create GPS point with MSL altitude
                gps_point = GeoPoint(lat_deg=wp_lat, lon_deg=wp_lon, alt_m=wp_alt_msl)
                
                # Convert to local NED
                local_ned = converter.gps_to_ned(gps_point)
                local_tuple = (local_ned.north, local_ned.east, local_ned.down)
                self._local_waypoints.append(local_tuple)
                
                logger.info(
                    f"{LogIcons.SUCCESS} WP{idx}: GPS({wp_lat:.7f}, {wp_lon:.7f}, {wp_alt_msl:.1f}m MSL) -> "
                    f"Local NED(N:{local_ned.north:.2f}m, E:{local_ned.east:.2f}m, D:{local_ned.down:.2f}m)"
                )
            
            self._converted_to_local = True
            
            # Compute trajectory using local waypoints
            logger.info(f"{LogIcons.WARNING} setpoint data: {self.__class__.__name__}: {self.setpoint_offset}")
            
            self.pos_traj_ids, self.pos_traj_json, self.yaw_traj_ids, self.yaw_traj_json = self._compute_trajectory(
                waypoints=self._local_waypoints,
                yaws_deg=self.step.yaws_deg,
                speed=self.step.speed,
                yaw_speed=self.step.yaw_speed,
                home=self.setpoint_offset.waypoint_offset,
                home_yaw=self.setpoint_offset.yaw_offset,
                cartesian=self.step.cartesian,
            )
            
            logger.info(f"{LogIcons.SUCCESS} GPS waypoints successfully converted and trajectory computed")
            
        except Exception as e:
            logger.error(f"{LogIcons.ERROR} Error in GotoGPSWaypointExecutor.start(): {e}")
            logger.error(traceback.format_exc())
            raise e


class GotoLocalPositionExecutor(_GotoExecutor):
    def __init__(self, step: GotoLocalPosition, setpointMemory: SetpointMemory, mission_id: Optional[str] = None, mavlink_proxy: MavLinkExternalProxy = None, redis_proxy: RedisProxy = None, fc_status_provider=None):
        super().__init__(step=step, setpointMemory=setpointMemory, mission_id=mission_id, mavlink_proxy=mavlink_proxy, redis_proxy=redis_proxy, fc_status_provider=fc_status_provider)


class GotoRelativeExecutor(_GotoExecutor):
    def __init__(self, step: GotoRelative, setpointMemory: SetpointMemory, mission_id: Optional[str] = None, mavlink_proxy: MavLinkExternalProxy = None, redis_proxy: RedisProxy = None, fc_status_provider=None):
        super().__init__(step=step, setpointMemory=setpointMemory, mission_id=mission_id, mavlink_proxy=mavlink_proxy, redis_proxy=redis_proxy, fc_status_provider=fc_status_provider)

    def start(self):
        setup_redis_subscriptions(pattern="/petal-leafsdk/notify_trajectory_completed", callback=self._handle_notify_trajectory_completed, redis_proxy=self.redis_proxy)
        try:
            # Cumulative sum the relative points to get absolute waypoints
            waypoints = np.cumsum(self.step.waypoints, axis=0) + self.setpoint_offset.waypoint_offset

            logger.debug(f"{LogIcons.WARNING} Using waypoint offset: {self.setpoint_offset.waypoint_offset} and yaw offset: {self.setpoint_offset.yaw_offset}")

            # Compute trajectory once
            self.pos_traj_ids, self.pos_traj_json, self.yaw_traj_ids, self.yaw_traj_json = self._compute_trajectory(
                                                                                                waypoints,
                                                                                                self.step.yaws_deg,
                                                                                                self.step.speed,
                                                                                                self.step.yaw_speed,
                                                                                                home=self.setpoint_offset.waypoint_offset,
                                                                                                home_yaw=self.setpoint_offset.yaw_offset,
                                                                                                cartesian=self.step.cartesian,
                                                                                                is_yaw_relative=True,
                                                                                            )
            
        except Exception as e:
            logger.error(f"{LogIcons.ERROR} Error computing trajectory: {e}")
            logger.error(traceback.format_exc())
            raise e
        

class YawAbsoluteExecutor(_GotoExecutor):
    def __init__(self, step: YawAbsolute, setpointMemory: SetpointMemory, mission_id: Optional[str] = None, mavlink_proxy: MavLinkExternalProxy = None, redis_proxy: RedisProxy = None, fc_status_provider=None):
        super().__init__(step=step, setpointMemory=setpointMemory, mission_id=mission_id, mavlink_proxy=mavlink_proxy, redis_proxy=redis_proxy, fc_status_provider=fc_status_provider)

    def start(self):
        setup_redis_subscriptions(pattern="/petal-leafsdk/notify_trajectory_completed", callback=self._handle_notify_trajectory_completed, redis_proxy=self.redis_proxy)
        try:
            logger.debug(f"{LogIcons.WARNING} Using waypoint offset: {self.setpoint_offset.waypoint_offset} and yaw offset: {self.setpoint_offset.yaw_offset}")

            waypoints = self.step.waypoints + np.asarray(self.setpoint_offset.waypoint_offset)

            # Compute trajectory once
            self.pos_traj_ids, self.pos_traj_json, self.yaw_traj_ids, self.yaw_traj_json = self._compute_trajectory(
                                                                                                waypoints,
                                                                                                self.step.yaws_deg,
                                                                                                self.step.speed,
                                                                                                self.step.yaw_speed,
                                                                                                home=self.setpoint_offset.waypoint_offset,
                                                                                                home_yaw=self.setpoint_offset.yaw_offset,
                                                                                                cartesian=self.step.cartesian,
                                                                                            )

        except Exception as e:
            logger.error(f"{LogIcons.ERROR} Error computing trajectory: {e}")
            logger.error(traceback.format_exc())
            raise e


class YawRelativeExecutor(_GotoExecutor):
    def __init__(self, step: YawRelative, setpointMemory: SetpointMemory, mission_id: Optional[str] = None, mavlink_proxy: MavLinkExternalProxy = None, redis_proxy: RedisProxy = None, fc_status_provider=None):
        super().__init__(step=step, setpointMemory=setpointMemory, mission_id=mission_id, mavlink_proxy=mavlink_proxy, redis_proxy=redis_proxy, fc_status_provider=fc_status_provider)

    def start(self):
        setup_redis_subscriptions(pattern="/petal-leafsdk/notify_trajectory_completed", callback=self._handle_notify_trajectory_completed, redis_proxy=self.redis_proxy)
        try:            
            logger.debug(f"{LogIcons.WARNING} Using waypoint offset: {self.setpoint_offset.waypoint_offset} and yaw offset: {self.setpoint_offset.yaw_offset}")

            waypoints = self.step.waypoints + np.asarray(self.setpoint_offset.waypoint_offset)
            # Compute trajectory once
            self.pos_traj_ids, self.pos_traj_json, self.yaw_traj_ids, self.yaw_traj_json = self._compute_trajectory(
                                                                                                waypoints,
                                                                                                self.step.yaws_deg,
                                                                                                self.step.speed,
                                                                                                self.step.yaw_speed,
                                                                                                home=self.setpoint_offset.waypoint_offset,
                                                                                                home_yaw=self.setpoint_offset.yaw_offset,
                                                                                                cartesian=self.step.cartesian,
                                                                                                is_yaw_relative=True
                                                                                            )
            
        except Exception as e:
            logger.error(f"{LogIcons.ERROR} Error computing trajectory: {e}")
            logger.error(traceback.format_exc())
            raise e


class TakeoffExecutor(MissionStepExecutor):
    """Takeoff step executor that waits for FC status change before completing."""
    
    POST_TAKEOFF_STABILIZATION_TIME = 2.0  # seconds to wait after FC reports flying
    DEFAULT_POST_IDLE_DELAY = 2.0  # default delay after successful idle (configurable via mission config)
    
    def __init__(self, step: Takeoff, setpointMemory: SetpointMemory, mission_id: Optional[str] = None, mavlink_proxy: MavLinkExternalProxy = None, redis_proxy: RedisProxy = None, fc_status_provider=None, mission_config=None):
        super().__init__(step=step, setpointMemory=setpointMemory, mission_id=mission_id, mavlink_proxy=mavlink_proxy, redis_proxy=redis_proxy, fc_status_provider=fc_status_provider)
        self._takeoff_command_sent = False
        self._initial_fc_status = None
        self._fc_flying_detected_time: Optional[float] = None  # When we first saw flying state
        self._idle_command_sent = False
        self._idle_success_time: Optional[float] = None  # When FC confirmed arm/idle
        self._mission_config = mission_config
        # Get post-idle delay from mission config, default to 2.0 seconds
        self._post_idle_delay = getattr(mission_config, 'post_idle_delay_seconds', self.DEFAULT_POST_IDLE_DELAY) if mission_config else self.DEFAULT_POST_IDLE_DELAY

    def setup(self):
        super().setup()
        self._takeoff_command_sent = False
        self._initial_fc_status = None
        self._fc_flying_detected_time = None
        self._idle_command_sent = False
        self._idle_success_time = None

    def start(self):
        # Capture initial FC status
        if self.fc_status_provider is not None:
            self._initial_fc_status = self.fc_status_provider.get_leaf_status()
            logger.info(f"{LogIcons.INFO} Initial FC status: {self.fc_status_provider.get_leaf_status_name()}")
            
            # If FC is READY_TO_FLY, send idle/arm command first
            if self._initial_fc_status == leafMAV.LEAF_STATUS_READY_TO_FLY:
                logger.info(f"{LogIcons.RUN} FC is READY_TO_FLY, sending ARM_IDLE command before takeoff...")
                self._send_arm_idle_command()
                self._idle_command_sent = True
                # Don't send takeoff yet - wait for idle confirmation in execute_step_logic
                return
        
        logger.info(f"{LogIcons.INFO} PRE-TAKEOFF setpoint offset: {self.setpoint_offset}")
        
        # FC is already armed or suitable state - send takeoff immediately
        self._send_takeoff_command()
    
    def _send_arm_idle_command(self) -> bool:
        """Send LEAF_DO_ARM_IDLE command to FC."""
        if self.mavlink_proxy is None:
            logger.warning(f"{LogIcons.WARNING} MavLinkExternalProxy is not provided, cannot send arm command.")
            return False
        
        msg = leafMAV.MAVLink_leaf_do_arm_idle_message(
            target_system=self.mavlink_proxy.target_system,
            enable=1  # 1 to arm/idle
        )
        self.mavlink_proxy.send(key='mav', msg=msg, burst_count=4, burst_interval=0.1)
        logger.info(f"{LogIcons.RUN} ARM_IDLE command sent to FC")
        return True
    
    def _send_takeoff_command(self) -> bool:
        """Send LEAF_DO_TAKEOFF command to FC."""
        if self.mavlink_proxy is None:
            logger.warning(f"{LogIcons.WARNING} MavLinkExternalProxy is not provided, cannot send takeoff message.")
            return False
        
        msg = leafMAV.MAVLink_leaf_do_takeoff_message(
            target_system=self.mavlink_proxy.target_system,
            altitude=self.step.alt
        )
        self.mavlink_proxy.send(key='mav', msg=msg, burst_count=4, burst_interval=0.1)
        self._takeoff_command_sent = True
        logger.info(f"{LogIcons.RUN} Takeoff command sent (target: {self.step.alt}m), waiting for FC status change + {self.POST_TAKEOFF_STABILIZATION_TIME}s stabilization...")
        return True

    def execute_step_logic(self) -> None:
        """Wait for FC status to change to flying state + stabilization delay before marking as completed."""
        if self.fc_status_provider is None:
            logger.warning(f"{LogIcons.WARNING} No FC status provider, marking takeoff complete immediately")
            self.state = StepState.PENDING_COMPLETION
            self.completion_state = StepCompletionState.SUCCESS
            return
        
        current_status = self.fc_status_provider.get_leaf_status()
        current_status_name = self.fc_status_provider.get_leaf_status_name()
        
        # If idle command was sent, wait for FC to arm, then wait post-idle delay
        if self._idle_command_sent and not self._takeoff_command_sent:
            # Check if FC has transitioned to ARMED_IDLE or ARMED
            if current_status in [leafMAV.LEAF_STATUS_ARMED_IDLE, leafMAV.LEAF_STATUS_ARMED]:
                if self._idle_success_time is None:
                    # First time detecting armed state
                    self._idle_success_time = time.time()
                    logger.info(f"{LogIcons.SUCCESS} FC armed successfully, waiting {self._post_idle_delay}s post-idle delay...")
                else:
                    # Check if post-idle delay has passed
                    elapsed = time.time() - self._idle_success_time
                    if elapsed >= self._post_idle_delay:
                        logger.info(f"{LogIcons.SUCCESS} Post-idle delay complete ({elapsed:.1f}s), sending takeoff command")
                        logger.info(f"{LogIcons.INFO} PRE-TAKEOFF setpoint offset: {self.setpoint_offset}")
                        self._send_takeoff_command()
                    else:
                        remaining = self._post_idle_delay - elapsed
                        logger.debug(f"{LogIcons.RUN} Post-idle delay... {remaining:.1f}s remaining")
            else:
                logger.debug(f"{LogIcons.RUN} Waiting for FC to arm... Current status: {current_status_name}")
            return
        
        # If takeoff command not sent yet (shouldn't happen, but safety check)
        if not self._takeoff_command_sent:
            logger.debug(f"{LogIcons.RUN} Waiting for takeoff command to be sent...")
            return
        
        # Consider takeoff complete when FC transitions to flying states
        flying_states = [
            leafMAV.LEAF_STATUS_TAKING_OFF,
            leafMAV.LEAF_STATUS_FLYING,
        ]
        
        if current_status in flying_states:
            # First time we detect flying state - start stabilization timer
            if self._fc_flying_detected_time is None:
                self._fc_flying_detected_time = time.time()
                logger.info(f"{LogIcons.SUCCESS} FC entered {current_status_name} - starting {self.POST_TAKEOFF_STABILIZATION_TIME}s stabilization wait...")
                logger.info(f"{LogIcons.INFO} Current setpoint offset at FC flying: {self.setpoint_offset}")
            
            # Check if stabilization time has passed
            elapsed = time.time() - self._fc_flying_detected_time
            if elapsed >= self.POST_TAKEOFF_STABILIZATION_TIME:
                logger.info(f"{LogIcons.SUCCESS} Takeoff stabilization complete ({elapsed:.1f}s elapsed)")
                logger.info(f"{LogIcons.INFO} POST-TAKEOFF setpoint offset: {self.setpoint_offset}")
                logger.info(f"{LogIcons.INFO} Setpoint update count: {self.setpoint_offset.update_counter}, last update: {time.time() - self.setpoint_offset.last_update_time:.2f}s ago")
                self.state = StepState.PENDING_COMPLETION
                self.completion_state = StepCompletionState.SUCCESS
            else:
                remaining = self.POST_TAKEOFF_STABILIZATION_TIME - elapsed
                logger.debug(f"{LogIcons.RUN} Takeoff stabilizing... {remaining:.1f}s remaining, current offset: {self.setpoint_offset.waypoint_offset}")
        else:
            # Reset flying detection if we somehow exit flying state
            if self._fc_flying_detected_time is not None:
                logger.warning(f"{LogIcons.WARNING} FC left flying state back to {current_status_name}, resetting stabilization timer")
                self._fc_flying_detected_time = None
            logger.debug(f"{LogIcons.RUN} Waiting for takeoff... FC status: {current_status_name}")


class WaitExecutor(MissionStepExecutor):
    def __init__(self, step: Wait, setpointMemory: SetpointMemory, mission_id: Optional[str] = None, mavlink_proxy: MavLinkExternalProxy = None, redis_proxy: RedisProxy = None, fc_status_provider=None):
        super().__init__(step=step, setpointMemory=setpointMemory, mission_id=mission_id, mavlink_proxy=mavlink_proxy, redis_proxy=redis_proxy, fc_status_provider=fc_status_provider)
        self.elapsed_before_pause = 0.0  # Track elapsed time before pause

    def is_pausable(self) -> bool:
        """Wait steps are always pausable with elapsed time tracking."""
        return True

    def start(self):
        self.tick = time.time()
        self.elapsed_before_pause = 0.0
        logger.info(f"{LogIcons.RUN} Wait step started, will wait for {self.step.duration} seconds")

    def execute_step_logic(self):
        elapsed_time = self.elapsed_before_pause + (time.time() - self.tick)
        remaining = self.step.duration - elapsed_time
        logger.debug(f"{LogIcons.RUN} Wait step executing: elapsed={elapsed_time:.2f}s, duration={self.step.duration}s, remaining={remaining:.2f}s")
        
        if elapsed_time >= self.step.duration:
            logger.info(f"{LogIcons.SUCCESS} Wait step duration reached, marking as completed")
            self.state = StepState.PENDING_COMPLETION
            self.completion_state = StepCompletionState.SUCCESS
    
    def pause(self) -> bool:
        """Pause the wait timer by saving elapsed time."""
        if self.is_pausable():
            if self.state == StepState.RUNNING:
                # Save elapsed time before pause
                self.elapsed_before_pause += (time.time() - self.tick)
                self.state = StepState.PAUSED
                logger.info(f"{LogIcons.PAUSE} Wait step paused: {self.description()} (elapsed: {self.elapsed_before_pause:.2f}s)")
                return True
            else:
                logger.warning(f"{LogIcons.WARNING} Step is not running, cannot pause: {self.description()}, state={self.state}")
                return False
        else:
            logger.warning(f"{LogIcons.WARNING} Step is not pausable: {self.description()}")
            return False
    
    def resume(self) -> bool:
        """Resume the wait timer from where it was paused."""
        if self.state == StepState.PAUSED:
            # Reset tick to current time to continue from pause point
            self.tick = time.time()
            logger.info(f"{LogIcons.RUN} Wait step resumed: {self.description()} (will wait {self.step.duration - self.elapsed_before_pause:.2f}s more)")
            self.state = StepState.RUNNING
            return True
        else:
            logger.warning(f"{LogIcons.WARNING} Step is not paused, cannot resume: {self.description()}")
            return False
    

class LandExecutor(MissionStepExecutor):
    def __init__(self, step: Land, setpointMemory: SetpointMemory, mission_id: Optional[str] = None, mavlink_proxy: MavLinkExternalProxy = None, redis_proxy: RedisProxy = None, fc_status_provider=None):
        super().__init__(step=step, setpointMemory=setpointMemory, mission_id=mission_id, mavlink_proxy=mavlink_proxy, redis_proxy=redis_proxy, fc_status_provider=fc_status_provider)
        self._landed = False

    def _handle_notify_trajectory_completed(self, channel: str, message: str) -> None:
        """
        Handle notification messages for landing trajectory completion.

        Parameters
        ----------
        channel : str
            The Redis channel from which the message was received.
        message : str
            The message content, expected to be a JSON string with trajectory details.
        """
        logger.info(f"{LogIcons.SUCCESS} Received notification on {channel}: {message}")

        try:
            command_data = json.loads(message)
            traj_id = command_data.get("trajectory_id")

            if "land" in traj_id:
                # For Land step, we can directly mark completed on any trajectory completion
                self._landed = True
                logger.info(f"{LogIcons.SUCCESS} Trajectory completed: {traj_id}")
        except Exception as e:
            logger.error(f"{LogIcons.ERROR} Error parsing completion notification: {e}")

    def start(self):
        super().start()
        setup_redis_subscriptions(pattern="/petal-leafsdk/notify_trajectory_completed", callback=self._handle_notify_trajectory_completed, redis_proxy=self.redis_proxy)
        if self.mavlink_proxy is not None:
            msg = leafMAV.MAVLink_leaf_do_land_message(
                target_system=self.mavlink_proxy.target_system,
            )
            self.mavlink_proxy.send(key='mav', msg=msg, burst_count=4, burst_interval=0.1)
        else:
            logger.warning(f"{LogIcons.WARNING} MavLinkExternalProxy is not provided, cannot send land message.")

    def execute_step_logic(self) -> None:
        if self._landed:
            self.state = StepState.PENDING_COMPLETION
            self.completion_state = StepCompletionState.SUCCESS

    def terminate(self):
        super().terminate()
        unsetup_redis_subscriptions(pattern="/petal-leafsdk/notify_trajectory_completed", redis_proxy=self.redis_proxy)
        self._landed = False
    

def get_mission_step_executor(step: MissionPlanStep, setpointMemory: SetpointMemory, mission_id: Optional[str] = None, mavlink_proxy: MavLinkExternalProxy = None, redis_proxy: RedisProxy = None, fc_status_provider=None, mission_config=None) -> MissionStepExecutor:
    """Factory method to get the appropriate MissionStepExecutor for a given MissionPlanStep."""
    if isinstance(step, GotoGPSWaypoint):
        return GotoGPSWaypointExecutor(step=step, setpointMemory=setpointMemory, mission_id=mission_id, mavlink_proxy=mavlink_proxy, redis_proxy=redis_proxy, fc_status_provider=fc_status_provider)
    elif isinstance(step, GotoLocalPosition):
        return GotoLocalPositionExecutor(step=step, setpointMemory=setpointMemory, mission_id=mission_id, mavlink_proxy=mavlink_proxy, redis_proxy=redis_proxy, fc_status_provider=fc_status_provider)
    elif isinstance(step, GotoRelative):
        return GotoRelativeExecutor(step=step, setpointMemory=setpointMemory, mission_id=mission_id, mavlink_proxy=mavlink_proxy, redis_proxy=redis_proxy, fc_status_provider=fc_status_provider)
    elif isinstance(step, YawAbsolute):
        return YawAbsoluteExecutor(step=step, setpointMemory=setpointMemory, mission_id=mission_id, mavlink_proxy=mavlink_proxy, redis_proxy=redis_proxy, fc_status_provider=fc_status_provider)
    elif isinstance(step, YawRelative):
        return YawRelativeExecutor(step=step, setpointMemory=setpointMemory, mission_id=mission_id, mavlink_proxy=mavlink_proxy, redis_proxy=redis_proxy, fc_status_provider=fc_status_provider)
    elif isinstance(step, Takeoff):
        return TakeoffExecutor(step=step, setpointMemory=setpointMemory, mission_id=mission_id, mavlink_proxy=mavlink_proxy, redis_proxy=redis_proxy, fc_status_provider=fc_status_provider, mission_config=mission_config)
    elif isinstance(step, Wait):
        return WaitExecutor(step=step, setpointMemory=setpointMemory, mission_id=mission_id, mavlink_proxy=mavlink_proxy, redis_proxy=redis_proxy, fc_status_provider=fc_status_provider)
    elif isinstance(step, Land):
        return LandExecutor(step=step, setpointMemory=setpointMemory, mission_id=mission_id, mavlink_proxy=mavlink_proxy, redis_proxy=redis_proxy, fc_status_provider=fc_status_provider)
    else:
        raise ValueError(f"Unsupported MissionPlanStep type: {type(step)}")