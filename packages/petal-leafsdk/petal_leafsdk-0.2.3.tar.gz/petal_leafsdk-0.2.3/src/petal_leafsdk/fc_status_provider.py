# petal_leafsdk/fc_status_provider.py
# FC Status Provider - self-contained FC status management with MAVLink handlers

import time
from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum, auto

from pymavlink import mavutil
from pymavlink.dialects.v20 import droneleaf_mav_msgs as leafMAV
from petal_app_manager.proxies.external import MavLinkExternalProxy

from leafsdk import logger
from leafsdk.utils.logstyle import LogIcons

from petal_leafsdk.coordinate_utils import GPSOrigin, CoordinateConverter, NEDPosition, HomePosition

# RTL Configuration Constants
RTL_MIN_ALTITUDE_M = 2.0  # Minimum altitude in meters for RTL operations


class DroneState(Enum):
    """High-level drone state abstraction mapped from LEAF_STATUS."""
    UNKNOWN = "unknown"
    DISARMED = "disarmed"
    IDLE = "idle"
    TAKEOFF = "takeoff"
    LANDING = "landing"
    MOVING = "moving"
    HOVERING = "hovering"
    SAFETY = "safety"
    
    @staticmethod
    def from_leaf_status(leaf_status: Optional[int]) -> 'DroneState':
        """Map LEAF_STATUS enum value to simplified DroneState."""
        if leaf_status is None:
            return DroneState.UNKNOWN
        
        status_map = {
            leafMAV.LEAF_STATUS_DISARMED: DroneState.DISARMED,
            leafMAV.LEAF_STATUS_READY_TO_FLY: DroneState.DISARMED,
            leafMAV.LEAF_STATUS_NOT_READY: DroneState.SAFETY,
            
            leafMAV.LEAF_STATUS_ARMED: DroneState.IDLE,
            leafMAV.LEAF_STATUS_ARMED_IDLE: DroneState.IDLE,
            
            leafMAV.LEAF_STATUS_TAKING_OFF: DroneState.TAKEOFF,
            
            leafMAV.LEAF_STATUS_FLYING: DroneState.MOVING,
            leafMAV.LEAF_STATUS_READY_TO_LEARN: DroneState.UNKNOWN,
            leafMAV.LEAF_STATUS_LEARNING: DroneState.UNKNOWN,
            
            leafMAV.LEAF_STATUS_LANDING: DroneState.LANDING,
            leafMAV.LEAF_STATUS_LANDED: DroneState.DISARMED,
            leafMAV.LEAF_STATUS_RETURNING_TO_BASE: DroneState.MOVING,
            
            leafMAV.LEAF_STATUS_MISSION_PAUSED: DroneState.HOVERING,
        }
        
        return status_map.get(leaf_status, DroneState.UNKNOWN)


class FCStatusProvider:    
    def __init__(self, mavlink_proxy: Optional[MavLinkExternalProxy] = None, 
                 on_status_change_callback=None,
                 on_mission_status_change=None):
        self._mavlink_proxy = mavlink_proxy
        self._on_status_change_callback = on_status_change_callback
        self._on_mission_status_change = on_mission_status_change
        
        # FC status state
        self._leaf_status: Optional[int] = None
        self._leaf_mission_status: Optional[int] = None
        self._leaf_mode: Optional[int] = None
        self._fc_armed: bool = False
        self._last_heartbeat_time: float = 0
        self._drone_state: DroneState = DroneState.UNKNOWN
        
        # Position data - owned and managed by FCStatusProvider
        self._gps_origin = GPSOrigin()  # GPS origin (can be from message or calculated)
        self._home_position = HomePosition()  # Home position (GPS + local NED)
        self._local_position = (0.0, 0.0, 0.0)  # (north, east, down) tuple
        self._last_local_position_time: float = 0  # Timestamp when local position was last updated
        
        # Logging throttling for position updates
        self._last_home_log_time: float = 0
        self._last_home_log_values: tuple = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        self._last_local_log_time: float = 0
        self._last_local_log_values: tuple = (0.0, 0.0, 0.0)
        
        # Register handlers if proxy provided
        if mavlink_proxy:
            self._register_mavlink_handlers()
    
    def set_mavlink_proxy(self, mavlink_proxy: MavLinkExternalProxy) -> bool:
        """Set MAVLink proxy and register handlers (for delayed initialization)."""
        if self._mavlink_proxy is not None:
            logger.warning(f"{LogIcons.WARNING} MAVLink proxy already set")
            return False
        self._mavlink_proxy = mavlink_proxy
        self._register_mavlink_handlers()
        return True
    
    def _register_mavlink_handlers(self):
        """Register all FC status-related MAVLink handlers."""
        if not self._mavlink_proxy:
            logger.warning(f"{LogIcons.WARNING} No MAVLink proxy available for FC status handlers")
            return
        
        handlers = {
            leafMAV.MAVLINK_MSG_ID_LEAF_STATUS: self._handle_leaf_status,
            leafMAV.MAVLINK_MSG_ID_LEAF_MISSION_STATUS: self._handle_leaf_mission_status,
            leafMAV.MAVLINK_MSG_ID_LEAF_MODE: self._handle_leaf_mode,
            leafMAV.MAVLINK_MSG_ID_LEAF_HEARTBEAT: self._handle_heartbeat,
            mavutil.mavlink.MAVLINK_MSG_ID_HOME_POSITION: self._handle_home_position,
            mavutil.mavlink.MAVLINK_MSG_ID_LOCAL_POSITION_NED: self._handle_local_position_ned,
            mavutil.mavlink.MAVLINK_MSG_ID_GPS_GLOBAL_ORIGIN: self._handle_gps_global_origin,
        }
        
        for msg_id, handler in handlers.items():
            self._mavlink_proxy.register_handler(
                key=str(msg_id),
                fn=handler,
                duplicate_filter_interval=0.7
            )
        
        logger.info(f"{LogIcons.SUCCESS} Registered {len(handlers)} FC status MAVLink handlers")
    
    # ===== MAVLink Message Handlers =====
    
    def _handle_leaf_status(self, msg: mavutil.mavlink.MAVLink_message) -> bool:
        """Handle LEAF_STATUS message from FC."""
        try:
            status_value = msg.status
            
            if self._leaf_status != status_value:
                prev_status = self._leaf_status
                self._leaf_status = status_value
                
                prev_drone_state = self._drone_state
                self._drone_state = DroneState.from_leaf_status(status_value)
                
                try:
                    status_name = leafMAV.enums['LEAF_STATUS'][status_value].name
                except (KeyError, AttributeError):
                    status_name = f'UNKNOWN_{status_value}'
                
                logger.info(
                    f"{LogIcons.SUCCESS} FC Status changed: {prev_status} -> {status_name} ({status_value}) | "
                    f"DroneState: {prev_drone_state.value} -> {self._drone_state.value}"
                )
                
                # Track armed state changes
                armed_states = [
                    leafMAV.LEAF_STATUS_ARMED_IDLE, leafMAV.LEAF_STATUS_ARMED,
                    leafMAV.LEAF_STATUS_TAKING_OFF, leafMAV.LEAF_STATUS_FLYING,
                    leafMAV.LEAF_STATUS_LANDING, leafMAV.LEAF_STATUS_RETURNING_TO_BASE,
                    leafMAV.LEAF_STATUS_MISSION_PAUSED,
                ]
                
                disarmed_states = [
                    leafMAV.LEAF_STATUS_DISARMED, leafMAV.LEAF_STATUS_READY_TO_FLY,
                    leafMAV.LEAF_STATUS_LANDED, leafMAV.LEAF_STATUS_NOT_READY,
                ]
                
                if status_value in armed_states and not self._fc_armed:
                    self._fc_armed = True
                    logger.info(f"{LogIcons.SUCCESS} FC is now ARMED (inferred from {status_name})")
                elif status_value in disarmed_states and self._fc_armed:
                    self._fc_armed = False
                    logger.info(f"{LogIcons.SUCCESS} FC is now DISARMED")
                
                # Notify plugin about status change requiring mission intervention
                if self._on_status_change_callback and self.should_pause_mission_on_fc_status():
                    logger.warning(f"{LogIcons.WARNING} FC entered {self._drone_state.value} state - mission may need intervention")
                    try:
                        self._on_status_change_callback()
                    except Exception as e:
                        logger.error(f"{LogIcons.ERROR} Error in status change callback: {e}")
            
            return True
        except Exception as e:
            logger.error(f"{LogIcons.ERROR} Error handling LEAF_STATUS message: {e}")
            return False
    
    def _handle_leaf_mission_status(self, msg: mavutil.mavlink.MAVLink_message) -> bool:
        """Handle LEAF_MISSION_STATUS message from FC."""
        try:
            mission_status_value = msg.status
            
            if self._leaf_mission_status != mission_status_value:
                prev_status = self._leaf_mission_status
                self._leaf_mission_status = mission_status_value
                
                try:
                    status_name = leafMAV.enums['LEAF_MISSION_STATE'][mission_status_value].name
                except (KeyError, AttributeError):
                    status_name = f'UNKNOWN_{mission_status_value}'
                
                logger.info(f"{LogIcons.SUCCESS} FC Mission Status changed: {prev_status} -> {status_name} ({mission_status_value})")
                
                # Notify distributed state observer
                if self._on_mission_status_change:
                    try:
                        self._on_mission_status_change(mission_status_value)
                    except Exception as e:
                        logger.error(f"{LogIcons.ERROR} Error in mission status change callback: {e}")
            
            return True
        except Exception as e:
            logger.error(f"{LogIcons.ERROR} Error handling LEAF_MISSION_STATUS message: {e}")
            return False
    
    def _handle_leaf_mode(self, msg: mavutil.mavlink.MAVLink_message) -> bool:
        """Handle LEAF_MODE message from FC."""
        try:
            mode_value = msg.mode
            
            if self._leaf_mode != mode_value:
                prev_mode = self._leaf_mode
                self._leaf_mode = mode_value
                
                try:
                    mode_name = leafMAV.enums['LEAF_MODE'][mode_value].name
                except (KeyError, AttributeError):
                    mode_name = f'UNKNOWN_{mode_value}'
                
                logger.info(f"{LogIcons.SUCCESS} FC Mode changed: {prev_mode} -> {mode_name} ({mode_value})")
            
            return True
        except Exception as e:
            logger.error(f"{LogIcons.ERROR} Error handling LEAF_MODE message: {e}")
            return False
    
    def _handle_heartbeat(self, msg: mavutil.mavlink.MAVLink_message) -> bool:
        """Handle LEAF_HEARTBEAT message - only tracks timing, not status/mode."""
        try:
            self._last_heartbeat_time = time.time()
            return True
        except Exception as e:
            logger.error(f"{LogIcons.ERROR} Error handling LEAF_HEARTBEAT message: {e}")
            return False
    
    def _handle_home_position(self, msg: mavutil.mavlink.MAVLink_message) -> bool:
        """Handle HOME_POSITION message (msg ID 242)."""
        try:
            if not self._home_position:
                logger.warning(f"{LogIcons.WARNING} Home position object not initialized")
                return False
            
            self._home_position.set_from_mavlink(
                lat=msg.latitude, lon=msg.longitude, alt=msg.altitude,
                x=msg.x, y=msg.y, z=msg.z
            )
            
            # Log periodically or on significant change
            now = time.time()
            current_values = (msg.latitude/1e7, msg.longitude/1e7, msg.altitude/1000.0, msg.x, msg.y, msg.z)
            last_values = self._last_home_log_values
            
            time_threshold_met = (now - self._last_home_log_time) >= 60.0
            position_changed = (
                abs(current_values[3] - last_values[3]) >= 0.5 or
                abs(current_values[4] - last_values[4]) >= 0.5 or
                abs(current_values[5] - last_values[5]) >= 0.5
            )
            
            if time_threshold_met or position_changed:
                self._last_home_log_time = now
                self._last_home_log_values = current_values
                logger.info(
                    f"{LogIcons.SUCCESS} Home position updated: "
                    f"GPS=({current_values[0]:.7f}, {current_values[1]:.7f}, {current_values[2]:.2f}m), "
                    f"Local NED=({current_values[3]:.2f}, {current_values[4]:.2f}, {current_values[5]:.2f})"
                )
            
            # Calculate origin from home if not set
            if self._gps_origin and not self._gps_origin.is_set:
                calculated_origin = GPSOrigin.calculate_from_home(self._home_position)
                
                if calculated_origin:
                    self._gps_origin = calculated_origin
                    logger.info(
                        f"{LogIcons.SUCCESS} GPS Origin calculated from home position: "
                        f"({self._gps_origin.gps.lat_deg:.7f}, {self._gps_origin.gps.lon_deg:.7f}, "
                        f"{self._gps_origin.gps.alt_m:.2f}m) [source: {self._gps_origin.source}]"
                    )
            
            return True
        except Exception as e:
            logger.error(f"{LogIcons.ERROR} Error handling HOME_POSITION message: {e}")
            return False
    
    def _handle_local_position_ned(self, msg: mavutil.mavlink.MAVLink_message) -> bool:
        """Handle LOCAL_POSITION_NED message (msg ID 32)."""
        try:
            now = time.time()
            self._local_position = (msg.x, msg.y, msg.z)
            self._last_local_position_time = now
            
            # Log periodically or on significant change
            current_values = (msg.x, msg.y, msg.z)
            last_values = self._last_local_log_values
            
            time_threshold_met = (now - self._last_local_log_time) >= 60.0
            position_changed = (
                abs(current_values[0] - last_values[0]) >= 0.5 or
                abs(current_values[1] - last_values[1]) >= 0.5 or
                abs(current_values[2] - last_values[2]) >= 0.5
            )
            
            if time_threshold_met or position_changed:
                self._last_local_log_time = now
                self._last_local_log_values = current_values
                logger.info(
                    f"{LogIcons.SUCCESS} Local position NED: ({current_values[0]:.2f}, {current_values[1]:.2f}, {current_values[2]:.2f})"
                )
            
            return True
        except Exception as e:
            logger.error(f"{LogIcons.ERROR} Error handling LOCAL_POSITION_NED message: {e}")
            return False
    
    def _handle_gps_global_origin(self, msg: mavutil.mavlink.MAVLink_message) -> bool:
        """Handle GPS_GLOBAL_ORIGIN message (msg ID 49)."""
        try:
            if not self._gps_origin:
                logger.warning(f"{LogIcons.WARNING} GPS origin object not initialized")
                return False
            
            self._gps_origin.set_from_mavlink(
                lat=msg.latitude, lon=msg.longitude, alt=msg.altitude
            )
            
            logger.info(
                f"{LogIcons.SUCCESS} GPS Origin set from message: "
                f"Lat={self._gps_origin.gps.lat_deg:.7f}, Lon={self._gps_origin.gps.lon_deg:.7f}, "
                f"Alt={self._gps_origin.gps.alt_m:.2f}m [source: {self._gps_origin.source}]"
            )
            
            return True
        except Exception as e:
            logger.error(f"{LogIcons.ERROR} Error handling GPS_GLOBAL_ORIGIN message: {e}")
            return False
    
    # ===== Getter Methods (for executors and plugin) =====
    
    def get_leaf_status(self) -> Optional[int]:
        """Get current LEAF_STATUS value."""
        return self._leaf_status
    
    def get_leaf_status_name(self) -> str:
        """Get current FC status as human-readable string."""
        if self._leaf_status is None:
            return "UNKNOWN (No status received)"
        try:
            return leafMAV.enums['LEAF_STATUS'][self._leaf_status].name
        except (KeyError, AttributeError):
            return f'UNKNOWN_{self._leaf_status}'
    
    def get_leaf_mission_status(self) -> Optional[int]:
        """Get current LEAF_MISSION_STATUS value."""
        return self._leaf_mission_status
    
    def get_leaf_mission_status_name(self) -> str:
        """Get current FC mission status as human-readable string."""
        if self._leaf_mission_status is None:
            return "UNKNOWN (No status received)"
        try:
            return leafMAV.enums['LEAF_MISSION_STATE'][self._leaf_mission_status].name
        except (KeyError, AttributeError):
            return f'UNKNOWN_{self._leaf_mission_status}'
    
    def get_leaf_mode(self) -> Optional[int]:
        """Get current LEAF_MODE value."""
        return self._leaf_mode
    
    def get_leaf_mode_name(self) -> str:
        """Get current FC mode as human-readable string."""
        if self._leaf_mode is None:
            return "UNKNOWN (No mode received)"
        try:
            return leafMAV.enums['LEAF_MODE'][self._leaf_mode].name
        except (KeyError, AttributeError):
            return f'UNKNOWN_{self._leaf_mode}'
    
    def is_fc_armed(self) -> bool:
        """Check if FC is armed."""
        return self._fc_armed
    
    def get_last_heartbeat_time(self) -> float:
        """Get timestamp of last heartbeat."""
        return self._last_heartbeat_time
    
    def get_heartbeat_age(self) -> float:
        """Get time since last heartbeat in seconds."""
        if self._last_heartbeat_time == 0:
            return float('inf')
        return time.time() - self._last_heartbeat_time
    
    def get_drone_state(self) -> DroneState:
        """Get current high-level drone state."""
        return self._drone_state
    
    def get_drone_state_value(self) -> str:
        """Get current drone state as string (for backward compatibility)."""
        return self._drone_state.value
    
    def get_gps_origin(self):
        """Get GPS origin object (GPSOrigin from coordinate_utils)."""
        return self._gps_origin
    
    def get_home_position(self):
        """Get home position object (HomePosition from coordinate_utils)."""
        return self._home_position
    
    def get_local_position(self) -> tuple:
        """Get current local position as (north, east, down) tuple."""
        return self._local_position
    
    def get_local_position_ned(self) -> Dict[str, float]:
        """Get current local position in NED frame as dict."""
        return {
            'north': self._local_position[0],
            'east': self._local_position[1],
            'down': self._local_position[2],
            'x': self._local_position[0],
            'y': self._local_position[1],
            'z': self._local_position[2],
        }
    
    def get_gps_origin_dict(self) -> Optional[Dict[str, Any]]:
        """Get GPS origin as dictionary."""
        if not self._gps_origin or not self._gps_origin.is_set or not self._gps_origin.gps:
            return None
        
        return {
            'lat_deg': self._gps_origin.gps.lat_deg,
            'lon_deg': self._gps_origin.gps.lon_deg,
            'alt_m': self._gps_origin.gps.alt_m,
            'lat_e7': self._gps_origin.gps.lat_e7,
            'lon_e7': self._gps_origin.gps.lon_e7,
            'alt_mm': self._gps_origin.gps.alt_mm,
            'is_set': self._gps_origin.is_set,
            'source': self._gps_origin.source,
        }
    
    def get_gps_from_local_position(self) -> Optional[Dict[str, Any]]:
        """Compute GPS position from local position + origin."""
        if not self._gps_origin or not self._gps_origin.is_set or not self._gps_origin.gps:
            return None
        
        try:
            converter = CoordinateConverter(origin=self._gps_origin.gps)
            ned_point = NEDPosition(
                north=self._local_position[0],
                east=self._local_position[1],
                down=self._local_position[2]
            )
            gps_point = converter.ned_to_gps(ned_point)
            
            return {
                'lat_deg': gps_point.lat_deg,
                'lon_deg': gps_point.lon_deg,
                'alt_m': gps_point.alt_m,
                'computed_from': 'local_position',
            }
        except Exception as e:
            logger.error(f"{LogIcons.ERROR} Error computing GPS from local position: {e}")
            return None
    
    def has_gps_origin(self) -> bool:
        """Check if GPS origin is available."""
        return self._gps_origin is not None and hasattr(self._gps_origin, 'is_set') and self._gps_origin.is_set
    
    def is_fc_connected(self, timeout: float = 3.0) -> bool:
        """Check if FC is connected based on heartbeat age."""
        return self.get_heartbeat_age() < timeout
    
    # ===== Status Check Methods =====
    
    def is_fc_in_status(self, status_value: int) -> bool:
        """Check if FC is in a specific LEAF_STATUS."""
        return self._leaf_status == status_value
    
    def is_drone_flying(self) -> bool:
        """Check if drone is in any flying state."""
        return self._drone_state in [DroneState.TAKEOFF, DroneState.MOVING, DroneState.HOVERING, DroneState.LANDING]
    
    def is_drone_landing(self) -> bool:
        """Check if drone is landing."""
        return self._drone_state == DroneState.LANDING
    
    def is_drone_in_safety_mode(self) -> bool:
        """Check if drone is in safety/emergency state."""
        return self._drone_state == DroneState.SAFETY
    
    def is_drone_safe_to_arm(self) -> bool:
        """Check if drone is in a state safe for arming."""
        return self._drone_state == DroneState.DISARMED and self.is_fc_connected()
    
    def is_drone_ready_for_mission(self) -> bool:
        """Check if drone is ready to start a mission."""
        return self._drone_state == DroneState.IDLE and self.is_fc_connected()
    
    def should_pause_mission_on_fc_status(self) -> bool:
        """Check if mission should be paused based on FC status."""
        return self._drone_state in [DroneState.SAFETY]
    
    def is_fc_available(self, max_age: float = 3.0) -> bool:
        """Check if FC is available based on heartbeat age (alias for is_fc_connected)."""
        return self.is_fc_connected(max_age)
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return (f"FCStatusProvider(leaf_status={self._leaf_status}, "
                f"drone_state={self._drone_state.value}, "
                f"armed={self._fc_armed}, "
                f"available={self.is_fc_available()})")
