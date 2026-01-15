# petal_leafsdk/mission.py
import json
from typing import Optional, Literal, Dict, Any, Tuple, TYPE_CHECKING
import traceback
from dataclasses import dataclass
import networkx as nx
from enum import Enum, auto
import asyncio, httpx
import uuid
import time
from petal_app_manager.proxies.external import MavLinkExternalProxy
from petal_app_manager.proxies.redis import RedisProxy
from petal_leafsdk.redis_helpers import subscribe_to_redis_channel, publish_to_redis_channel, publish_to_redis_channels, RedisChannels
from petal_leafsdk.mavlink_helpers import setup_mavlink_subscriptions, unsetup_mavlink_subscriptions
from petal_leafsdk.setpoint_memory import SetpointMemory
from pymavlink.dialects.v20 import droneleaf_mav_msgs as leafMAV
from pymavlink import mavutil
from leafsdk.core.mission.mission_plan import MissionPlan, JoystickMode, MissionConfig
from leafsdk.utils.logstyle import LogIcons
from leafsdk import logger
from petal_leafsdk.mission_step import get_mission_step_executor, StepState

if TYPE_CHECKING:
    from petal_leafsdk.fsm import CentralizedStatusManager

Tuple3D = Tuple[float, float, float]

class StatelessMissionFunctions:
    @staticmethod
    # def get_execution_graph(plan: MissionPlan) -> nx.MultiDiGraph:
    def generate_execution_graph_from_graph(graph: nx.MultiDiGraph, setpointMemory: SetpointMemory, mission_id: Optional[str] = None, mavlink_proxy: MavLinkExternalProxy = None, redis_proxy: RedisProxy = None, fc_status_provider=None, mission_config=None) -> nx.MultiDiGraph:
        """Generate the execution graph from the mission plan."""
        # Traverse and replace steps with their step executors
        for name, data in graph.nodes(data=True):
            step = data['step']
            step_executor = get_mission_step_executor(step, setpointMemory=setpointMemory, mission_id=mission_id, mavlink_proxy=mavlink_proxy, redis_proxy=redis_proxy, fc_status_provider=fc_status_provider, mission_config=mission_config)
            graph.nodes[name]['step'] = step_executor
        return graph
    
    def apply_joystick_mode(mission_config: MissionConfig, redis_proxy: RedisProxy):
        """Apply joystick mode setting from mission plan to Redis."""
        if mission_config is None:
            logger.warning(f"{LogIcons.WARNING} No mission config loaded. Using default joystick mode.")
            from leafsdk.core.mission.mission_plan import MissionConfig
            mission_config = MissionConfig()
        
        joystick_cmd = mission_config.joystick_mode.value
        redis_proxy.publish(
            channel="/FlightLogic/joystick_mode",
            message=json.dumps({"payload": joystick_cmd})
        )
        logger.info(f"{LogIcons.SUCCESS} Joystick control set to {mission_config.joystick_mode.name}.")

    def apply_mission_state(
        mission_state: 'MissionStateAll',
        mission_id: str,
        queue_count: int,
        joystick_mode: int,
        predefined_actions_status: int,
        redis_proxy: RedisProxy
    ):
        """Publish mission state to Redis (outgoing status broadcast)."""
        status_data = {
            "mission_status": mission_state.value,
            "mission_status_name": mission_state.name,
            "joystick_mode": joystick_mode,
            "mission_id": mission_id,
            "queue_count": queue_count,
            "predefined_actions_status": predefined_actions_status,
        }
        redis_proxy.publish(
            channel="/FlightLogic/set_mission_state",
            message=json.dumps(status_data)
        )
        logger.debug(f"{LogIcons.SUCCESS} Published mission state to Redis: {mission_state.name}")

    
    async def publish_status_update_httpx(subscriber_address, status: dict):
        if subscriber_address:
            try:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    await client.post(
                        subscriber_address,
                        json=status,
                        headers={"Content-Type": "application/json"},
                    )
            except Exception as e:
                logger.warning(f"{LogIcons.WARNING} Failed to report progress: {e}")

    def publish_status_update_redis(redis_proxy: RedisProxy, current_mission_graph_id, current_mission_executor, status: Dict[str, Any]) -> None:
        if redis_proxy is None or current_mission_graph_id is None:
            return

        # Use the stored mission graph ID for consistency
        mission_id = current_mission_graph_id
        
        # Verify it matches the mission ID (stored in Mission, not MissionPlan)
        current_mission_id = getattr(current_mission_executor, 'id', None)
        if current_mission_id and current_mission_id != mission_id:
            logger.warning(f"{LogIcons.WARNING} Mission ID mismatch: graph_id='{mission_id}' vs mission.id='{current_mission_id}'")
        
        message_id = f"mission-progress-{uuid.uuid4()}"
        timestamp = time.time()

        if True: #publish mission status update
            progress_payload = {
                "message_id": message_id,
                "mission_id": mission_id,
                "timestamp": timestamp,
                "status": status,
                "source": "petal-leafsdk",
            }

            try:
                serialized_progress = json.dumps(progress_payload)
            except Exception as exc:
                logger.error(f"{LogIcons.ERROR} Failed to serialize mission progress payload: {exc}")
                return

            channels = [
                RedisChannels.REDIS_PROGRESS_CHANNEL.value,
                f"{RedisChannels.REDIS_PROGRESS_CHANNEL.value}/{mission_id}",
            ]

            for channel in channels:
                try:
                    redis_proxy.publish(channel=channel, message=serialized_progress)
                except Exception as exc:
                    logger.warning(f"{LogIcons.WARNING} Failed to publish mission progress on {channel}: {exc}")


        if status.get("next_step_id") or status.get("step_id"): #publish leg status updates
            leg_payload = {
                "message_id": message_id,
                "mission_id": mission_id,
                "timestamp": timestamp,
                "current_step_id": status.get("next_step_id"),
                "previous_step_id": status.get("step_id"),
                "state": status.get("state"),
                "step_completed": status.get("step_completed"),
                "source": "petal-leafsdk",
            }

            try:
                serialized_leg = json.dumps(leg_payload)
            except Exception as exc:
                logger.error(f"{LogIcons.ERROR} Failed to serialize mission leg payload: {exc}")
                return

            leg_channels = [
                RedisChannels.REDIS_MISSION_LEG_CHANNEL.value,
                f"{RedisChannels.REDIS_MISSION_LEG_CHANNEL.value}/{mission_id}",
            ]

            for channel in leg_channels:
                try:
                    redis_proxy.publish(channel=channel, message=serialized_leg)
                except Exception as exc:
                    logger.warning(f"{LogIcons.WARNING} Failed to publish mission leg update on {channel}: {exc}")


class Mission:
    """Mission execution controller.
    
    Architecture:
    - mission_plan: MissionPlan instance (contains name, id, config, graph)
    - execution_graph: NetworkX graph with executable step instances
    - mission_status: Current execution state
    
    The mission_plan.name is used for duplicate detection in queue.
    - The mission_plan.name is used for duplicate detection in queue (has UUID suffix).
    - The Mission.id is an independent unique identifier generated at load time.
    """
    def __init__(self, mav_proxy: MavLinkExternalProxy, redis_proxy: RedisProxy, data: dict | str = None, fc_status_provider=None, setpoint_offset: SetpointMemory = None, status_manager: Optional['CentralizedStatusManager'] = None):
        self.mission_plan = None  # MissionPlan instance (will be created in load_plan)
        self.execution_graph = None  # Executable graph with step instances
        self.mav_proxy = mav_proxy
        self.redis_proxy = redis_proxy
        self.fc_status_provider = fc_status_provider
        self.mission_status = MissionStatus()
        self.current_step = None
        self.current_node = None
        self.prev_step = None
        self.prev_node = None
        # Use shared setpoint_offset from plugin (no handler registration here)
        self.setpoint_offset = setpoint_offset if setpoint_offset is not None else SetpointMemory()
        self.plan_data = data  # Raw mission data (dict from MissionPlanDTO)
        
        # Centralized status management
        self._centralized_status_manager = status_manager
        self._centralized_status_mission = None
        if status_manager:
            from petal_leafsdk.fsm import Centralized_Status_Mission
            self._centralized_status_mission = Centralized_Status_Mission("CENTRALIZED_STATUS_MISSION", status_manager)
            self._centralized_status_mission.register()
            logger.info(f"{LogIcons.SUCCESS} Mission: Centralized_Status_Mission registered")
    
    @property
    def mission_name(self) -> Optional[str]:
        """Get mission name from plan (used for duplicate checking)."""
        return self.mission_plan.name if self.mission_plan else None
    
    @property
    def mission_id(self) -> Optional[str]:
        """Get unique mission ID (independent from plan, generated at load time)."""
        return self.id
    
    @property
    def mission_config(self):
        """Get mission config from plan."""
        return self.mission_plan.config if self.mission_plan else None

    def load_plan(self, data: dict | str | None = None) -> bool:
        """Load a new mission plan.
        
        Creates a MissionPlan instance from the data, which handles:
        - Setting plan.name from data["name"] with UUID suffix
        - Generating unique Mission.id (independent from plan name)
        - Loading config and graph
        """
        # only allow if no mission is running
        if self.mission_status.get_state() != MissionStateAll.IDLE:
            logger.warning(f"{LogIcons.WARNING} Cannot load new mission plan while another mission is in state: {self.mission_status.get_state().name}.")
            return False

        if data is None:
            data = self.plan_data
        
        try:
            self.mission_plan = MissionPlan()
            self.mission_plan.load(data)
            
            # Generate unique mission ID (independent from plan name)
            self.id = str(uuid.uuid4())
            
            # Validate the plan
            errors = self.mission_plan.validate()
            if errors:
                raise ValueError(f"Invalid mission plan: {errors}")
            
            mission_graph = self.mission_plan.mission_graph.copy()
            
            if not mission_graph.nodes:
                raise ValueError("Mission plan is empty. Cannot prepare for execution.")
            
            # Generate execution graph with step instances
            self.execution_graph = StatelessMissionFunctions.generate_execution_graph_from_graph(
                mission_graph, 
                setpointMemory=self.setpoint_offset, 
                mission_id=self.id,  # Use Mission's unique ID, not plan name
                mavlink_proxy=self.mav_proxy, 
                redis_proxy=self.redis_proxy, 
                fc_status_provider=self.fc_status_provider,
                mission_config=self.mission_config  # Pass mission config for Takeoff step
            )
            
            self.current_node = next(iter(self.execution_graph.nodes()), None)
            self.current_step = self.execution_graph.nodes[self.current_node]['step']
            self.mission_status.set_state(MissionStateAll.READY)
            
            logger.info(f"{LogIcons.SUCCESS} Mission plan '{self.mission_name}' (ID: {self.mission_id}) loaded successfully with config: {self.mission_config.to_dict()}")
            return True
            
        except Exception as e:
            logger.error(f"{LogIcons.ERROR} Failed to load mission plan: {e}")
            logger.error(traceback.format_exc())
            return False

    async def publish_status_update(self, current_mission_graph_id, subscriber_address):
        status = self.gen_dict_status()
        await StatelessMissionFunctions.publish_status_update_httpx(subscriber_address, status)
        StatelessMissionFunctions.publish_status_update_redis(self.redis_proxy, current_mission_graph_id, self, status)


    def run_step(self) -> bool: # completed a step, or completed entire mission
        logger.debug(f"{LogIcons.RUN} run_step called: state={self.mission_status.get_state().name}, node={self.current_node}")
        # we can access step state via self.current_step.state: StepState, which could be {IDLE, RUNNING, PAUSED, COMPLETED}
        # code style:
        ## condition:
        ### internal action
        ### internal state update (if needed)
        ### log
        ### return True (step/mission completed or no mission) or False (step/mission still running)

        if self.mission_status.is_completed():
            logger.info(f"{LogIcons.SUCCESS} Mission already completed with state: {self.mission_status.get_state().name}. No further execution.")
            return True
        if self.mission_status.get_state() == MissionStateAll.IDLE:
            logger.warning(f"{LogIcons.WARNING} No mission loaded. Cannot execute steps.")
            return True  # nothing to do

        if self.mission_status.get_state() == MissionStateAll.READY:
            # Start the mission
            self.mission_status.set_state(MissionStateAll.RUNNING)
            logger.info(f"{LogIcons.RUN} Mission started. Beginning execution at step: {self.current_node}")
            return False  # mission just started, step not completed yet
        
        if self.mission_status.get_state() == MissionStateAll.PAUSED_BETWEEN_STEPS:
            logger.info(f"{LogIcons.PAUSE} Mission is paused between steps. Current step: {self.current_node}.")
            return False  # mission paused, step not completed yet

        # should not be called as this condition is handled at the time of step completion below
        if self.mission_status.get_state() == MissionStateAll.SCHEDULED_PAUSE and self.current_step is not None and self.current_step.state == StepState.IDLE:
            logger.warning(f"{LogIcons.ERROR} Scheduled pause between steps is possible now, however, it is been caught at unexpected location. Applying at: {self.current_node}.")
            self.mission_status.set_state(MissionStateAll.PAUSED_BETWEEN_STEPS)
            return False  # mission paused, step not completed yet

        if self.setpoint_offset.update_counter == 0:  # do not start mission until we have at least one setpoint offset
            logger.info(f"{LogIcons.PAUSE} Waiting for initial setpoint offset before executing step: {self.current_node}.")
            return False  # mission paused, step not completed yet

        try:
            result, completed_step = self.current_step.execute_step()
        except Exception as e:
            logger.error(f"{LogIcons.ERROR} Step {self.current_node} failed: {e}\n{traceback.format_exc()}")
            self.mission_status.set_state(MissionStateAll.FAILED)
            return False # it will be marked as completed in the next call

        if completed_step:
            logger.info(f"{LogIcons.SUCCESS} Step {self.current_step.description()} completed (node: {self.current_node})")
            self.prev_node = self.current_node
            self.prev_step = self.current_step
            self.current_node = self.get_next_node(self.prev_node, result)
            if self.current_node is None: # also helps preventing pause at end of mission
                logger.info(f"{LogIcons.SUCCESS} No next node found, mission completing...")
                self.mission_status.set_state(MissionStateAll.COMPLETED)
                return True
            else:
                self.current_step = self.execution_graph.nodes[self.current_node]['step']
                if self.mission_status.get_state() == MissionStateAll.SCHEDULED_PAUSE:
                    self.mission_status.set_state(MissionStateAll.PAUSED_BETWEEN_STEPS)
                    logger.info(f"{LogIcons.PAUSE} Mission paused after completion of step: {self.current_node}")
                    return True
                else:
                    logger.info(f"{LogIcons.RUN} Transitioning to next step: {self.current_node}")
                    self.mission_status.set_state(MissionStateAll.RUNNING)
                    return True
        else:
            # Step not completed yet, continue running
            return False


    def get_next_node(self, prev_node: str, expected_condition) -> Optional[str]:
        """Determine the next node based on current node and conditions."""
        next_node = None
        for successor in self.execution_graph.successors(prev_node):
            condition = self.execution_graph.edges[prev_node, successor, 0].get("condition")
            if condition is None or condition == expected_condition:
                next_node = successor
                break
        return next_node

    def pause(self, action: Optional[Literal["NONE"]] = "NONE") -> bool:
        """Pause the mission execution."""
        logger.info(f"{LogIcons.RUN} Mission pause commanded.")

        if self.current_step is None: # We can use this to pause in between steps
            logger.warning(f"{LogIcons.WARNING} Cannot pause, no current step to pause.")
            return False

        if self.mav_proxy is None: # should not be the case, ever
            logger.warning(f"{LogIcons.WARNING} Cannot pause, MAVLink proxy is required.")
            return False

        if self.mission_status.get_state() != MissionStateAll.RUNNING:
            logger.warning(f"{LogIcons.WARNING} Mission cannot be paused, current state: {self.mission_status.get_state().name}.")
            return False
        
        if self.current_step.state == StepState.IDLE: # We can use this to pause in between steps
            result = self.mission_status.set_state(MissionStateAll.SCHEDULED_PAUSE) # Use scheduled pause to do the pause in the run function
            logger.info(f"{LogIcons.RUN} Mission will pause before starting the next step.")
            return result # True if state changed

        if self.current_step.pause(): # try immediate pause
            # ToDo: await FC confirmation
            self.mission_status.set_state(MissionStateAll.PAUSED_MID_STEP)
            logger.info(f"{LogIcons.PAUSE} Mission paused immediately (mid-step)")
            return True
        else:
            self.mission_status.set_state(MissionStateAll.SCHEDULED_PAUSE)
            logger.info(f"{LogIcons.RUN} Mission will pause after the step is completed.")
            return False

    def resume(self):
        """Resume the mission execution."""
        logger.info(f"{LogIcons.RUN} Mission resume commanded.")
        if self.mission_status.get_state() in [MissionStateAll.SCHEDULED_PAUSE, MissionStateAll.PAUSED_BETWEEN_STEPS, MissionStateAll.PAUSED_MID_STEP]:
            logger.info(f"{LogIcons.RUN} Resuming mission from paused state: {self.mission_status.get_state().name}.")
            self.mission_status.set_state(MissionStateAll.RUNNING)
            # also pass the resume to current step, but no action is expected there
            if self.current_step is not None:
                self.current_step.resume()
            return True
        if self.current_step is None: # We paused in between steps
            logger.warning(f"{LogIcons.WARNING} Cannot resume, no current step to resume.")
            return False
        if self.mav_proxy is None: # should not be the case, ever
            logger.warning(f"{LogIcons.WARNING} Cannot resume, MAVLink proxy is required.")
            return False
        if self.mission_status.get_state() in [MissionStateAll.RUNNING]:
            result = self.current_step.resume()
            return result
        logger.warning(f"{LogIcons.WARNING} Mission cannot be resumed, current state: {self.mission_status.get_state().name}.")
        return False

    def abort(self):
        """Abort the mission execution completely."""
        self.mission_status.set_state(MissionStateAll.CANCELLED)  # TODO: Consider adding ABORTED state
        if self.current_step is not None:
            try:
                self.current_step.cancel()  # Step still uses cancel internally
            except Exception as e:
                logger.error(f"{LogIcons.ERROR} Failed to abort current step: {e}")
            logger.info(f"{LogIcons.CANCEL} Mission aborted at step: {self.current_node}")
        return True
            
    # def reset(self): 
    #     """Reset the mission to its initial state."""
    #     self.execution_graph = None
    #     self.mission_status.reset()
    #     if self.current_step is not None:
    #         self.current_step.cancel()
    #     self.current_step = None
    #     self.current_node = None
    #     self.prev_step = None
    #     self.prev_node = None
    #     self.current_mission_id = None
    #     logger.info(f"{LogIcons.SUCCESS} Mission has been reset.")

    def gen_dict_status(self) -> dict:
        """Get the current mission status as a dictionary."""
        output = {
            "mission_id": self.mission_id,
            "mission_config": self.mission_config.to_dict() if self.mission_config else None,
            "step_id": self.prev_node,
            "step_description": self.prev_step.description() if self.prev_step else None,
            "next_step_id": self.current_node,
            "next_step_description": self.current_step.description() if self.current_step else None,
            "state": str(self.mission_status.get_state().name),
        }
        return output


class MissionStateAll(Enum):
    """Mission states matching LEAF_MISSION_STATE MAVLink enum."""
    IDLE = leafMAV.LEAF_MISSION_STATE_IDLE                          # 0: Queue is empty, no mission loaded
    READY = leafMAV.LEAF_MISSION_STATE_READY                        # 1: Current mission is ready to execute
    RUNNING = leafMAV.LEAF_MISSION_STATE_RUNNING                    # 2: Current mission is running
    SCHEDULED_PAUSE = leafMAV.LEAF_MISSION_STATE_SCHEDULED_PAUSE    # 3: Running but has a scheduled pause
    PAUSED_MID_STEP = leafMAV.LEAF_MISSION_STATE_PAUSED_MID_STEP    # 4: Paused mid-step
    PAUSED_BETWEEN_STEPS = leafMAV.LEAF_MISSION_STATE_PAUSED_BETWEEN_STEPS  # 5: Paused between steps
    COMPLETED = leafMAV.LEAF_MISSION_STATE_COMPLETED                # 6: Mission completed successfully
    FAILED = leafMAV.LEAF_MISSION_STATE_FAILED                      # 7: Mission failed
    CANCELLED = leafMAV.LEAF_MISSION_STATE_CANCELLED                # 8: Mission was cancelled
    SAFETY = leafMAV.LEAF_MISSION_STATE_SAFETY                      # 9: Critical safety state, FC decides
    
    def __str__(self):
        return self.name

    def is_in_progress(self) -> bool:
        """Check if the mission state indicates running."""
        return self in [MissionStateAll.RUNNING, MissionStateAll.SCHEDULED_PAUSE]

    def is_currently_paused(self) -> bool:
        """Check if the mission state indicates paused."""
        return self in [MissionStateAll.PAUSED_MID_STEP, MissionStateAll.PAUSED_BETWEEN_STEPS]
    
    def is_completed(self) -> bool:
        """Check if the mission state indicates completed (successful or failed)."""
        return self in [MissionStateAll.COMPLETED, MissionStateAll.CANCELLED, MissionStateAll.FAILED, MissionStateAll.SAFETY]
    def is_mission_loaded(self) -> bool:
        """Check if a mission is loaded (not in IDLE state)."""
        return self != MissionStateAll.IDLE and not self.is_completed()


@dataclass
class MissionStatus():
    state: MissionStateAll = MissionStateAll.IDLE
    
    def set_state(self, state: MissionStateAll) -> bool:
        """Set the current mission state. Returns True if state changed."""

        force_one_way = [MissionStateAll.COMPLETED, MissionStateAll.CANCELLED, MissionStateAll.FAILED]
        if self.state in force_one_way and state not in force_one_way:
            logger.warning(f"{LogIcons.WARNING} Mission state change from {self.state} to {state} is not allowed.")
            return False

        _state = self.get_state()
        self.state = state
        # update step_completed based on state, it is one way! to unset, call reset
        if state in [MissionStateAll.COMPLETED, MissionStateAll.CANCELLED, MissionStateAll.FAILED]:
            pass # step completed
        return _state != self.get_state()
    
    def get_state(self) -> MissionStateAll:
        """Get the current mission state."""
        return self.state
    
    def is_in_progress(self) -> bool:
        return self.state.is_in_progress()
    
    def is_currently_paused(self) -> bool:
        return self.state.is_currently_paused()
    
    def is_completed(self) -> bool:
        return self.state.is_completed()
    
    def reset(self):
        """Reset mission status to initial state."""
        self.state = MissionStateAll.IDLE