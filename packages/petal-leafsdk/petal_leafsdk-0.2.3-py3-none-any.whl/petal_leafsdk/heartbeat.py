"""
Mission Manager Heartbeat Service

Publishes periodic heartbeat messages to Redis to indicate the mission manager is alive.
Follows the same pattern as petal-app-manager's health status publisher.
"""

import asyncio
import time
import json
import logging
from typing import Optional

from petal_app_manager.proxies.redis import RedisProxy
from leafsdk.utils.logstyle import LogIcons

logger = logging.getLogger(__name__)


class MissionManagerHeartbeat:
    """
    Manages periodic heartbeat publishing for the mission manager.
    
    Publishes at 10Hz to Redis channel indicating the mission manager is alive.
    """
    
    def __init__(
        self,
        redis_proxy: RedisProxy,
        frequency_hz: float = 10.0,
        channel: str = "/mission-manager/heartbeat"
    ):
        """
        Initialize the heartbeat service.
        
        Args:
            redis_proxy: Redis proxy instance for publishing
            frequency_hz: Heartbeat frequency in Hz (default: 10.0)
            channel: Redis channel to publish heartbeat on
        """
        self.redis_proxy = redis_proxy
        self.frequency_hz = frequency_hz
        self.interval = 1.0 / frequency_hz  # Convert Hz to seconds
        self.channel = channel
        self._running = False
        self._task: Optional[asyncio.Task] = None
        
    async def start(self):
        """Start the heartbeat publishing loop."""
        if self._running:
            logger.warning(f"{LogIcons.WARNING} Heartbeat already running")
            return
            
        if not self.redis_proxy:
            logger.error(f"{LogIcons.ERROR} Cannot start heartbeat - Redis proxy not available")
            return
            
        self._running = True
        self._task = asyncio.create_task(self._heartbeat_loop())
        logger.info(
            f"{LogIcons.SUCCESS} Mission Manager heartbeat started "
            f"(frequency: {self.frequency_hz}Hz, channel: {self.channel})"
        )
    
    async def stop(self):
        """Stop the heartbeat publishing loop."""
        if not self._running:
            return
            
        self._running = False
        
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        
        logger.info(f"{LogIcons.INFO} Mission Manager heartbeat stopped")
    
    async def _heartbeat_loop(self):
        """Main heartbeat publishing loop."""
        logger.info(f"{LogIcons.RUN} Starting heartbeat loop (interval: {self.interval:.3f}s)")
        
        while self._running:
            try:
                # Create heartbeat message
                heartbeat_message = self._create_heartbeat_message()
                
                # Publish to Redis channel
                message_json = json.dumps(heartbeat_message)
                result = self.redis_proxy.publish(self.channel, message_json)
                
                if result > 0:
                    logger.debug(
                        f"{LogIcons.PUBLISH} Published heartbeat to {self.channel} "
                        f"({result} subscribers)"
                    )
                else:
                    logger.debug(
                        f"{LogIcons.PUBLISH} Published heartbeat to {self.channel} "
                        f"(no subscribers)"
                    )
                    
            except Exception as e:
                logger.error(f"{LogIcons.ERROR} Error publishing heartbeat: {e}")
            
            # Wait for next heartbeat interval
            await asyncio.sleep(self.interval)
    
    def _create_heartbeat_message(self) -> dict:
        """
        Create the heartbeat message payload.
        
        Returns:
            Dictionary containing heartbeat data
        """
        return {
            "timestamp": time.time(),
            "state": "TODO",  # TODO: Update with actual mission manager state
            "service": "petal-leafsdk",
            "component": "mission-manager",
            "status": "alive"
        }
