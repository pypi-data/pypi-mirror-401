# leafsdk/utils/mavlink_helpers.py
# MAVLink helper functions for LeafSDK

import sys, time
import os
from pymavlink.dialects.v20 import droneleaf_mav_msgs as leafMAV
from petal_app_manager.proxies.external import MavLinkExternalProxy
from leafsdk import logger
from typing import Optional, Union
from leafsdk.utils.logstyle import LogIcons


class MissionActionCode:
    """Action codes for mission control commands sent to flight controller."""
    NONE = 0  # TODO: renamed from NONE to SAFETY
    HOVER = 1
    RETURN_TO_HOME = 2
    LAND_IMMEDIATELY = 3


class MAVLinkCommand:
    """Command codes for MAVLink leaf_control_cmd messages."""
    PAUSE = 0
    RESUME = 1
    CANCEL = 2


class MAVLinkConstants:
    """Constants for MAVLink protocol and mission execution behavior."""
    MISSION_ID_MAX_LENGTH = 20  # Maximum length for mission ID before truncation
    MAVLINK_BURST_COUNT = 4     # Number of times to send MAVLink messages
    MAVLINK_BURST_INTERVAL = 0.1  # Interval between burst messages in seconds
    FC_CANCEL_WAIT_TIME = 0.5   # Time to wait for FC to process cancel command


def get_mav_msg_name_from_id(msg_id: int) -> Union[str, int]:
    """
    Get MAVLink message name from its ID.
    """
    try:
        msg_name = leafMAV.mavlink_map[msg_id].name
        return msg_name
    except KeyError:
        logger.warning(f"{LogIcons.WARNING} Unknown MAVLink message ID: {msg_id}")
        return msg_id

def parse_heartbeat(msg):
    """
    Parse heartbeat message and return system status info.
    """
    if msg.get_type() != "HEARTBEAT":
        logger.warning("Expected HEARTBEAT message, got something else.")
        return None

    status = {
        "type": msg.type,
        "autopilot": msg.autopilot,
        "base_mode": msg.base_mode,
        "custom_mode": msg.custom_mode,
        "system_status": msg.system_status,
        "mavlink_version": msg.mavlink_version,
    }
    logger.debug(f"Parsed heartbeat: {status}")
    return status

def setup_mavlink_subscriptions(key: str, callback: callable, mav_proxy: Optional[MavLinkExternalProxy] = None, duplicate_filter_interval: Optional[float] = 0):
    """Setup MAVLink subscriptions - call this after object creation if using MAVLink"""
    if mav_proxy is None:
        logger.warning(f"{LogIcons.WARNING} MAVLink proxy not provided, skipping MAVLink subscriptions")
        return
        
    try:
        # Subscribe to a general broadcast channel
        mav_proxy.register_handler(
            key=key,
            fn=callback,
            duplicate_filter_interval=duplicate_filter_interval
        )

        logger.info(f"{LogIcons.SUCCESS} MAVLink subscriptions set up successfully to {get_mav_msg_name_from_id(int(key))}.")
    except Exception as e:
        logger.error(f"{LogIcons.ERROR} Failed to set up MAVLink subscriptions: {e}")

def unsetup_mavlink_subscriptions(key: str, callback: callable, mav_proxy: Optional[MavLinkExternalProxy] = None):
    """Unsubscribe from MAVLink channels - call this when the step is no longer needed"""
    if mav_proxy is None:
        logger.warning(f"{LogIcons.WARNING} MAVLink proxy not provided, skipping MAVLink unsubscriptions")
        return
        
    try:
        mav_proxy.unregister_handler(key=key, fn=callback)
        logger.info(f"{LogIcons.SUCCESS} MAVLink subscriptions to {get_mav_msg_name_from_id(int(key))} have been removed.")
    except Exception as e:
        logger.error(f"{LogIcons.ERROR} Failed to remove MAVLink subscriptions: {e}")


def extract_mission_id_from_msg(msg) -> Optional[str]:
    """
    Extract mission ID from MAVLink message - handles both string and bytes.
    
    Args:
        msg: MAVLink message with mission_id attribute
        
    Returns:
        Mission ID as string, or None if extraction fails
    """
    try:
        if hasattr(msg, 'mission_id'):
            mission_id_raw = msg.mission_id
            if isinstance(mission_id_raw, bytes):
                return mission_id_raw.decode('ascii').rstrip('\x00')
            elif isinstance(mission_id_raw, str):
                return mission_id_raw.rstrip('\x00')
            else:
                return str(mission_id_raw).rstrip('\x00')
        return None
    except Exception as e:
        logger.warning(f"{LogIcons.WARNING} Failed to extract mission ID: {e}")
        return None


def send_mavlink_message(mav_proxy: Optional[MavLinkExternalProxy], msg, description: str, 
                         burst_count: int = 3, burst_interval: float = 0.01) -> bool:
    """
    Send a MAVLink message to the flight controller.
    
    Args:
        mav_proxy: MAVLink proxy to send message through
        msg: The MAVLink message to send
        description: Description for logging
        burst_count: Number of times to send the message (default: 3)
        burst_interval: Time between bursts in seconds (default: 0.01)
    
    Returns:
        True if message sent successfully, False otherwise
    """
    if mav_proxy is None:
        logger.warning(f"{LogIcons.WARNING} Cannot send {description} - MAVLink proxy unavailable")
        return False
    
    try:
        mav_proxy.send(
            key='mav', 
            msg=msg, 
            burst_count=burst_count, 
            burst_interval=burst_interval
        )
        logger.info(f"{LogIcons.RUN} Sent {description}")
        return True
    except Exception as e:
        logger.error(f"{LogIcons.ERROR} Failed to send {description}: {e}")
        return False