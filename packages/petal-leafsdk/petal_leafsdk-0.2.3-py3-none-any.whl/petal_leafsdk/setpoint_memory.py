# petal_leafsdk/setpoint_memory.py
"""Setpoint memory data structure for tracking MAVLink setpoint offsets."""

import time
from dataclasses import dataclass, field
from typing import Tuple
from pymavlink import mavutil
from leafsdk import logger
from leafsdk.utils.logstyle import LogIcons

Tuple3D = Tuple[float, float, float]


@dataclass
class SetpointMemory:
    """Stores setpoint offsets received from MAVLink messages."""
    
    yaw_offset: float = 0.0
    waypoint_offset: Tuple3D = (0.0, 0.0, 0.0)
    update_counter: int = field(default=0, init=False)
    last_update_time: float = field(default_factory=time.time, init=False)
    
    def handler_setpoint(self, msg: mavutil.mavlink.MAVLink_message) -> bool:
        """Handle incoming setpoint position message from MAVLink."""
        self.yaw_offset = msg.yaw
        self.waypoint_offset = (msg.x, msg.y, msg.z)
        self.update_counter += 1
        self.last_update_time = time.time()
        logger.debug(f"{LogIcons.SUCCESS} Received setpoint position: {self}")
        return True
