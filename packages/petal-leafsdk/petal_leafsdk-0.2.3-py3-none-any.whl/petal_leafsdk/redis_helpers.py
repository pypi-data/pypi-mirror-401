# petal_leafsdk/redis_helpers.py
# Redis helper functions for petal-leafsdk

from enum import Enum
from leafsdk import logger
from leafsdk.utils.logstyle import LogIcons
from petal_app_manager.proxies.redis import RedisProxy
from pydantic import BaseModel
from typing import Optional, Callable, List


class RedisChannels(str, Enum):
    """Redis channel constants for QGC mission adapter communication."""
    REDIS_CMD_CHANNEL = "/petal/qgc_mission_adapter/cmd"
    REDIS_ACK_CHANNEL = "/petal/qgc_mission_adapter/ack"
    REDIS_PROGRESS_CHANNEL = "/petal/qgc_mission_adapter/progress"
    REDIS_MISSION_LEG_CHANNEL = "/petal/qgc_mission_adapter/mission_leg"


# Pattern-based subscriptions (original functions)
def setup_redis_subscriptions(pattern: str, callback: callable, redis_proxy: Optional[RedisProxy] = None):
    """Setup Redis subscriptions - call this after object creation if using Redis"""
    if redis_proxy is None:
        logger.warning(f"{LogIcons.WARNING} Redis proxy not provided, skipping Redis subscriptions")
        return False
        
    try:
        # Subscribe to a general broadcast channel
        redis_proxy.register_pattern_channel_callback(channel=pattern, callback=callback)

        logger.info(f"{LogIcons.SUCCESS} Redis subscriptions set up successfully to {pattern}.")
        return True
    except Exception as e:
        logger.error(f"{LogIcons.ERROR} Failed to set up Redis subscriptions: {e}")
        return False

def unsetup_redis_subscriptions(pattern: str, redis_proxy: Optional[RedisProxy] = None):
    """Unsubscribe from Redis channels - call this when the step is no longer needed"""
    if redis_proxy is None:
        logger.warning(f"{LogIcons.WARNING} Redis proxy not provided, skipping Redis unsubscriptions")
        return   False
        
    try:
        redis_proxy.unregister_pattern_channel_callback(channel=pattern)
        logger.info(f"{LogIcons.SUCCESS} Redis subscriptions to {pattern} have been removed.")
        return True
    except Exception as e:
        logger.error(f"{LogIcons.ERROR} Failed to remove Redis subscriptions: {e}")
        return False

# Exact channel subscriptions
def subscribe_to_redis_channel(
    channel: str,
    callback: Callable[[str, str], None],
    redis_proxy: Optional[RedisProxy] = None,
) -> bool:
    """
    Subscribe to an exact Redis channel.
    
    Args:
        channel: The channel name to subscribe to
        callback: Function to call when a message is received (channel, data)
        redis_proxy: Redis proxy instance
    
    Returns:
        True if subscription succeeded, False otherwise
    """
    if redis_proxy is None:
        logger.warning(f"{LogIcons.WARNING} Redis proxy not provided, skipping subscription to {channel}")
        return False

    try:
        redis_proxy.subscribe(channel, callback)
        logger.info(f"{LogIcons.SUCCESS} Subscribed to Redis channel: {channel}")
        return True
    except Exception as e:
        logger.error(f"{LogIcons.ERROR} Failed to subscribe to Redis channel {channel}: {e}")
        return False


def publish_to_redis_channel(
    channel: str,
    message: BaseModel,
    redis_proxy: Optional[RedisProxy] = None,
) -> bool:
    """
    Publish a Pydantic model to a Redis channel.
    
    Args:
        channel: The channel to publish to
        message: Pydantic model to serialize and publish
        redis_proxy: Redis proxy instance
    
    Returns:
        True if publish succeeded, False otherwise
    """
    if redis_proxy is None:
        return False

    try:
        serialized = message.model_dump_json()
    except Exception as exc:
        logger.error(f"{LogIcons.ERROR} Failed to serialize message for {channel}: {exc}")
        return False

    try:
        redis_proxy.publish(channel=channel, message=serialized)
        return True
    except Exception as exc:
        logger.error(f"{LogIcons.ERROR} Failed to publish to {channel}: {exc}")
        return False


def publish_to_redis_channels(
    channels: List[str],
    message: BaseModel,
    redis_proxy: Optional[RedisProxy] = None,
) -> bool:
    """
    Publish a Pydantic model to multiple Redis channels.
    
    Args:
        channels: List of channels to publish to
        message: Pydantic model to serialize and publish
        redis_proxy: Redis proxy instance
    
    Returns:
        True if all publishes succeeded, False if any failed
    """
    if redis_proxy is None:
        return False

    try:
        serialized = message.model_dump_json()
    except Exception as exc:
        logger.error(f"{LogIcons.ERROR} Failed to serialize message: {exc}")
        return False

    all_success = True
    for channel in channels:
        try:
            redis_proxy.publish(channel=channel, message=serialized)
        except Exception as exc:
            logger.warning(f"{LogIcons.WARNING} Failed to publish to {channel}: {exc}")
            all_success = False

    return all_success

