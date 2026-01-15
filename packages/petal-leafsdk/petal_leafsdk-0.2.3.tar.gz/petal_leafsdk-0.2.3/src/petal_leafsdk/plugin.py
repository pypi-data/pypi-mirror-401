import time
import json
import uuid
from . import logger

from typing import Any, Dict, Optional, Literal
import asyncio, httpx
import traceback

from pymavlink.dialects.v20 import droneleaf_mav_msgs as leafMAV
from pymavlink import mavutil

from petal_app_manager.plugins.base import Petal
from petal_app_manager.plugins.decorators import http_action
from petal_app_manager.proxies.external import MavLinkExternalProxy
from petal_app_manager.proxies import (
    RedisProxy,
    MQTTProxy,
)

from petal_leafsdk.data_model import (
    MissionPlanDTO, ProgressUpdateSubscription, JoystickModeRequest,
    RedisCommandPayload, RedisAckPayload, RedisProgressPayload, RedisMissionLegPayload,
    MQTTCommandMessage, MQTTResponseMessage, GotoRequest
)
from petal_leafsdk.redis_helpers import subscribe_to_redis_channel, publish_to_redis_channel, publish_to_redis_channels, RedisChannels
from petal_leafsdk.mission import Mission, MissionStateAll
from petal_leafsdk.mission_queue import MissionQueue
from petal_leafsdk.fc_status_provider import FCStatusProvider, DroneState, RTL_MIN_ALTITUDE_M
from petal_leafsdk.heartbeat import MissionManagerHeartbeat
from petal_leafsdk.distributed_memory_state import DistributedMemoryState
from petal_leafsdk.mavlink_helpers import (
    extract_mission_id_from_msg, send_mavlink_message,
    MissionActionCode, MAVLinkCommand, MAVLinkConstants
)

from leafsdk.core.mission.mission_clock import MissionClock
from leafsdk.core.mission.mission_plan import (
    MissionPlan,
    MissionConfig,
    JoystickMode,
    MissionLoadBehavior,
    AllowDuplicateNames,
    AutoStartBehavior,
    MissionSuccessfulCompletionBehavior,
    MissionUnsuccessfulCompletionBehavior
)
from leafsdk.utils.logstyle import LogIcons
from petal_leafsdk.setpoint_memory import SetpointMemory
from enum import Enum
from petal_leafsdk.mission import StatelessMissionFunctions
from petal_leafsdk.fsm import (
    CentralizedStatusManager,
    Centralized_Status_FC
)

class MissionManager(Petal):  # TODO:
    """
    Mission Manager Plugin - Manages mission execution and FC coordination.
    
    ORGANIZATION:
    ══════════════════════════════════════════════════════════════════════
    §1.  Initialization & Setup
    §2.  Status & State Helpers
    §3.  Event Handlers (Cross-Proxy)
    §4.  Mission Loading & Validation
    §5.  Mission Execution Flow
    §6.  Mission Control Operations
    §7.  FC Communication (MAVLink Senders)
    §8.  Status Publishing
    §9.  HTTP Web API Endpoints
    §10. Redis Command Handlers
    §11. MQTT Command Handlers
    ══════════════════════════════════════════════════════════════════════
    
    Note: FC status getters accessed via self._fc_status_provider directly
    """
    name = "petal-leafsdk" # TODO: petal-mission-manager  
    version = "v0.2.3"
    use_mqtt_proxy = True  # Enable MQTT-aware startup

    
    # ══════════════════════════════════════════════════════════════════
    # §1. INITIALIZATION & SETUP
    # ══════════════════════════════════════════════════════════════════
    
    def startup(self):
        super().startup()
        self.subscriber_address = None # For progress updates
        self.safe_return_waypoint_request_address = None # For safe return waypoint requests
        self.mqtt_subscription_id = None

        self._redis_proxy: RedisProxy = None
        self._mqtt_proxy: MQTTProxy = None
        self._mavlink_proxy: MavLinkExternalProxy = None

        # Initialize centralized status manager FIRST (before creating Queue/Mission)
        self._centralized_status_manager = CentralizedStatusManager()
        self._centralized_status_manager.start()
        
        # MissionManager only owns the FC status module
        self._centralized_status_fc = Centralized_Status_FC("CENTRALIZED_STATUS_FC", self._centralized_status_manager)
        self._centralized_status_fc.register()

        # MissionQueue creates and owns its own Centralized_Status_Queue
        self.previous_missions = MissionQueue(max_size=50)  
        self.mission_queue = MissionQueue(
            max_size=10,
            previous_missions=self.previous_missions,
            status_manager=self._centralized_status_manager,  # Pass manager to queue
        )
        
        self.setpoint_offset = SetpointMemory()
        
        # Initialize FC mission state tracker (distributed memory state)
        self._distributed_mission_state: DistributedMemoryState[MissionStateAll] = DistributedMemoryState(
            initial_state=MissionStateAll.IDLE,
            on_propose_action=self._do_fc_mission_action,
            on_mismatch_action=self._on_fc_mission_state_mismatch
        )
        
        self._fc_status_provider = FCStatusProvider(
            mavlink_proxy=None,  # Will be set in async_startup
            on_status_change_callback=self._on_fc_status_change,
            on_mission_status_change=self._on_fc_mission_status_update
        )

        self.mission_clock = None   # initialized in async_startup
        self._event_loop = asyncio.get_event_loop()  # store loop reference
        self._abort_ack_event = asyncio.Event()  # Event to signal abort ACK received
        self._heartbeat: Optional[MissionManagerHeartbeat] = None  # Heartbeat service
        
        # Mission runner loop control
        self._is_runner_active = False  # Flag to control runner loop
        self._mission_runner_task: Optional[asyncio.Task] = None  # Runner loop task
        
        logger.info(f"{LogIcons.SUCCESS} CentralizedStatusManager initialized with FC module (Queue/Mission manage their own)")
    
    async def async_startup(self):
        """
        Called after startup to handle async operations like MQTT subscriptions.
        
        Note: The MQTT-aware startup logic (organization ID monitoring, event loop setup)
        is handled by the main application's _mqtt_aware_petal_startup function.
        This method will be called by that function after organization ID is available.
        """
        logger.info("{LogIcons.RUN} Performing async startup...")

        self._redis_proxy = self._proxies.get("redis")
        self._mqtt_proxy = self._proxies.get("mqtt")
        self._mavlink_proxy = self._proxies.get("ext_mavlink")
        
        self._fc_status_provider.set_mavlink_proxy(self._mavlink_proxy)
        
        await self._setup_mqtt_topics()
        self._setup_mavlink_handlers()
        self._init_mavlink()
        self._setup_redis_command_listener()   
        self.mission_clock = MissionClock(rate_hz=50)
        
        # # Initialize and start heartbeat service
        # if self._redis_proxy:
        #     self._heartbeat = MissionManagerHeartbeat(
        #         redis_proxy=self._redis_proxy,
        #         frequency_hz=10.0,
        #         channel="/mission-manager/heartbeat"
        #     )
        #     await self._heartbeat.start()
        # else:
        #     logger.warning(f"{LogIcons.WARNING} Redis proxy not available - heartbeat disabled")
        
        # Start the continuous mission runner loop
        self._is_runner_active = True
        self._mission_runner_task = asyncio.create_task(self._mission_runner_loop())
        self._mavlink_heartbeat_task = asyncio.create_task(self._mavlink_heartbeat_loop())
        logger.info(f"{LogIcons.SUCCESS} Mission runner loop & MAVLink heartbeat started")
    
    async def async_shutdown(self):
        """
        Called before shutdown to handle async cleanup operations.
        """
        logger.info(f"{LogIcons.INFO} Performing async shutdown...")
        
        # Stop heartbeat service
        if self._heartbeat:
            await self._heartbeat.stop()
            logger.info(f"{LogIcons.SUCCESS} Heartbeat service stopped")
        
        # Stop mission runner loop
        self._is_runner_active = False
        if self._mission_runner_task:
            self._mission_runner_task.cancel()
            try:
                await self._mission_runner_task
            except asyncio.CancelledError:
                pass
            logger.info(f"{LogIcons.SUCCESS} Mission runner loop stopped")

        if hasattr(self, '_mavlink_heartbeat_task') and self._mavlink_heartbeat_task:
            self._mavlink_heartbeat_task.cancel()
            try:
                await self._mavlink_heartbeat_task
            except asyncio.CancelledError:
                pass
            logger.info(f"{LogIcons.SUCCESS} MAVLink heartbeat loop stopped")
        
        logger.info(f"{LogIcons.SUCCESS} Async shutdown completed")
    
    async def _setup_mqtt_topics(self):
        logger.info(f"{LogIcons.RUN} Setting up MQTT topics...")
        await self._mqtt_subscribe_to_mission_plan()
        logger.info(f"{LogIcons.SUCCESS} All MQTT topics active")
    
    def _setup_mavlink_handlers(self):
        """Setup mission-specific MAVLink handlers (FC status handlers are in FCStatusProvider)."""
        self._mavlink_handlers = {}

        def _handler_setpoint_offset(msg: mavutil.mavlink.MAVLink_message) -> bool:
            """Handle setpoint offset messages for active mission."""
            return self.setpoint_offset.handler_setpoint(msg)
        
        def _handler_mavlink_mission_run_ack(msg: mavutil.mavlink.MAVLink_message) -> bool:
            """Called when the FC acknowledges mission start. This triggers mission execution."""
            ack_mission_id = extract_mission_id_from_msg(msg)
            return self._handle_mission_run_ack(ack_mission_id)
        
        def _handler_mavlink_qgc_control_cmd(msg: mavutil.mavlink.MAVLink_message) -> bool:
            """Handle QGC mission control commands using LEAF_MISSION_CONTROL_COMMAND enum."""
            control_cmd_name = leafMAV.enums['LEAF_MISSION_CONTROL_COMMAND'][msg.cmd].name
            # Handle both bytes and string for mission_id
            mission_id_raw = msg.mission_id if hasattr(msg, 'mission_id') else None
            if isinstance(mission_id_raw, bytes):
                mission_id = mission_id_raw.decode('utf-8').rstrip('\x00')
            elif isinstance(mission_id_raw, str):
                mission_id = mission_id_raw.rstrip('\x00')
            else:
                mission_id = None
            logger.info(f"{LogIcons.SUCCESS} Received QGC mission control command: {control_cmd_name} for mission '{mission_id}'")

            if msg.cmd == leafMAV.LEAF_MISSION_CONTROL_PAUSE:
                self.pause()
            elif msg.cmd == leafMAV.LEAF_MISSION_CONTROL_RESUME:
                self.resume()
            elif msg.cmd == leafMAV.LEAF_MISSION_CONTROL_ABORT:
                self.abort()
            elif msg.cmd == leafMAV.LEAF_MISSION_CONTROL_START:
                self.start_mission(mission_id)
            elif msg.cmd == leafMAV.LEAF_MISSION_CONTROL_READY:
                logger.info(f"{LogIcons.INFO} READY command received - mission already loaded")
            elif msg.cmd == leafMAV.LEAF_MISSION_CONTROL_LAND_IN_PLACE:
                self.land_in_place()
            elif msg.cmd == leafMAV.LEAF_MISSION_CONTROL_RETURN_TO_LAUNCH:
                self.return_to_launch()
            
            return True
        
        def _handler_mavlink_ack_mission_abort(msg: mavutil.mavlink.MAVLink_message) -> bool:
            """Handle abort acknowledgment."""
            logger.info(f"{LogIcons.SUCCESS} Received MAVLink mission abort acknowledgment from flight controller.")
            self._abort_ack_event.set()  # Signal that abort ACK was received
            # NOTE: Not triggering mission completion here - let state machine handle it
            return True
        
        def _handler_mavlink_ack_mission_resume(msg: mavutil.mavlink.MAVLink_message) -> bool:
            """Handle resume acknowledgment."""
            logger.info(f"{LogIcons.SUCCESS} Received MAVLink mission resume acknowledgment from flight controller.")
            return True
        
        self._mavlink_handlers[leafMAV.MAVLINK_MSG_ID_LEAF_SETPOINT_OFFSET] = _handler_setpoint_offset
        self._mavlink_handlers[leafMAV.MAVLINK_MSG_ID_LEAF_ACK_MISSION_RUN] = _handler_mavlink_mission_run_ack
        self._mavlink_handlers[leafMAV.MAVLINK_MSG_ID_LEAF_DO_QGC_MISSION_CONTROL_CMD] = _handler_mavlink_qgc_control_cmd
        self._mavlink_handlers[leafMAV.MAVLINK_MSG_ID_LEAF_ACK_MISSION_ABORT] = _handler_mavlink_ack_mission_abort
        self._mavlink_handlers[leafMAV.MAVLINK_MSG_ID_LEAF_ACK_MISSION_RESUME] = _handler_mavlink_ack_mission_resume

    def _init_mavlink(self):
        logger.info(f"{LogIcons.RUN} Initializing MAVLink connection via proxy...")
        
        for msg_id, handler in self._mavlink_handlers.items():
            self._mavlink_proxy.register_handler(
                key=str(msg_id),
                fn=handler,
                duplicate_filter_interval=0.7
            )
        
        logger.info(
            f"{LogIcons.SUCCESS} Registered {len(self._mavlink_handlers)} mission-specific MAVLink handlers"
        )
    
    def _setup_redis_command_listener(self):
        if self._redis_proxy is None:
            logger.warning(f"{LogIcons.WARNING} Redis proxy unavailable — QGC mission adapter commands disabled.")
            return False

        try:
            self._redis_proxy.subscribe(RedisChannels.REDIS_CMD_CHANNEL.value, self._handle_redis_command_message)
            logger.info(
                f"{LogIcons.SUCCESS} Subscribed to QGC mission adapter channel: {RedisChannels.REDIS_CMD_CHANNEL.value}"
            )
            return True
        except Exception as exc:
            logger.error(f"{LogIcons.ERROR} Failed to subscribe to QGC mission adapter channel: {exc}")
            return False
    
    
    # ══════════════════════════════════════════════════════════════════
    # §2. STATUS & STATE HELPERS
    # ══════════════════════════════════════════════════════════════════
    
    def _has_active_mission(self) -> bool:
        """Check if there's an active mission (queue not empty)."""
        return not self.mission_queue.is_empty()
    
    def _is_mission_in_progress(self) -> bool:
        """Check if mission is currently executing."""
        mission = self.mission_queue.get_current_mission()
        if mission is None:
            return False
        return mission.mission_status.is_in_progress()
    
    
    # ══════════════════════════════════════════════════════════════════
    # §3. EVENT HANDLERS (Cross-Proxy)
    # ══════════════════════════════════════════════════════════════════
    
    def _on_fc_status_change(self):
        """Callback from FCStatusProvider when FC enters state requiring mission intervention."""
        # Push update through centralized manager
        fc_data = {
            "fc_connected": self._fc_status_provider.is_connected,
            "drone_state": self._fc_status_provider.drone_state.name if self._fc_status_provider.drone_state else None,
            "battery_level": getattr(self._fc_status_provider, 'battery_level', 100.0),
        }
        self._centralized_status_fc.update(fc_data)
        
        if self._is_mission_in_progress():
            # TODO: Consider auto-pausing mission based on configuration
            pass
    
    def _do_fc_mission_action(self, proposed_state: MissionStateAll):
        """Execute FC command for proposed mission state (triggered by propose()).
        
        This sends the state to FC via LEAF_SET_MISSION_STATE message.
        All state changes go through here - no separate pause/resume/run functions.
        """
        mission_id = self.mission_queue.get_current_mission_id()
        
        # For IDLE state, allow sending even without active mission (for cleanup)
        if not mission_id and proposed_state != MissionStateAll.IDLE:
            logger.warning(f"{LogIcons.WARNING} Cannot send FC command: no active mission")
            return
        
        # Use empty mission_id for IDLE cleanup if no active mission
        if not mission_id:
            mission_id = ""
        
        # Send state directly to FC - FC will handle the state transition
        self._send_state_to_fc(proposed_state, mission_id)
        logger.info(f"{LogIcons.RUN} Sent state {proposed_state.name} to FC for mission '{mission_id or '(cleanup)'}'")
    
    
    def _on_fc_mission_state_mismatch(self, remote_state: MissionStateAll):
        """Handle FC mission state mismatch - FC reported unexpected state."""
        proposed = self._distributed_mission_state.proposed_state
        current = self._distributed_mission_state.current_state
        
        logger.warning(
            f"{LogIcons.WARNING} FC mission state mismatch! "
            f"Local: {current.name}, "
            f"Proposed: {proposed.name if proposed else 'None'}, "
            f"Remote: {remote_state.name}"
        )
        
        # ACTION: If we have a pending proposal that differs from remote, RE-SEND IT.
        # This enforces our desired state ("always set state").
        if proposed is not None and proposed != remote_state:
            logger.info(f"{LogIcons.RUN} Mismatch detected: Re-sending proposed state {proposed.name} to FC...")
            self._do_fc_mission_action(proposed)
        else:
            # If no proposal (settled state), or proposal matches remote (convergence).
            # Handle specifically the case where Local is IDLE but Remote is RUNNING/PAUSED (orphaned mission on FC).
            if current == MissionStateAll.IDLE and remote_state in [MissionStateAll.RUNNING, MissionStateAll.PAUSED_MID_STEP, MissionStateAll.PAUSED_BETWEEN_STEPS, MissionStateAll.SCHEDULED_PAUSE]:
                logger.warning(f"{LogIcons.WARNING} Mismatch: Local is IDLE but Remote is {remote_state.name}. Aborting orphaned mission on FC.")
                # Properly abort the mission: RUNNING → CANCELLED → IDLE
                self._send_abort_to_fc()
                # Update our local state to expect CANCELLED
                self._distributed_mission_state._current_state = MissionStateAll.CANCELLED
                # Then propose IDLE (will be sent after FC confirms CANCELLED)
                self._distributed_mission_state.propose(MissionStateAll.IDLE)
            elif current == MissionStateAll.IDLE and remote_state == MissionStateAll.READY:
                logger.warning(f"{LogIcons.WARNING} Mismatch: Local is IDLE but Remote is READY. Forcing FC to IDLE.")
                # Force FC back to IDLE when local is IDLE but FC is READY (startup state mismatch)
                self._distributed_mission_state.propose(MissionStateAll.IDLE)
            else:
                 # Otherwise sync local to remote (handles external state changes)
                 self._distributed_mission_state.sync_to_remote()
    
    def _on_fc_mission_status_update(self, mission_status_value: int):
        """Called when FC reports LEAF_MISSION_STATUS change - update distributed state."""
        # Direct lookup since MissionStateAll values match LEAF_MISSION_STATE
        try:
            mission_state = MissionStateAll(mission_status_value)
        except ValueError:
            logger.warning(f"{LogIcons.WARNING} Unknown mission status value: {mission_status_value}")
            mission_state = MissionStateAll.IDLE
        
        self._distributed_mission_state.update_remote_state(mission_state)
        
        # If state matches proposed, confirm the transition
        if self._distributed_mission_state.proposed_state == mission_state:
            self._distributed_mission_state.confirm()
        
        # Note: IDLE transition after terminal states is now handled synchronously
        # in _mission_completion() before the mission is dequeued


    def _handle_mission_run_ack(self, ack_mission_id: str) -> bool:
        if not ack_mission_id:
            logger.error(f"{LogIcons.ERROR} Received mission ACK with no mission ID")
            return False
        if ack_mission_id != self.mission_queue.get_current_mission_id():
            logger.error(
                f"{LogIcons.ERROR} Mission ID mismatch in ACK! "
                f"Expected: '{self.mission_queue.get_current_mission_id()}', Got: '{ack_mission_id}'"
            )
            return False
        if self._is_mission_in_progress():
            logger.info(
                f"{LogIcons.WARNING} Mission '{ack_mission_id}' is already in progress. "
                f"Ignoring duplicate ACK."
            )
            return False
        try:
            logger.info(f"{LogIcons.RUN} Starting mission execution for ID: '{ack_mission_id}'")
            if self.mission_queue.get_current_mission() is not None:
                self.mission_queue.get_current_mission().mission_status.set_state(MissionStateAll.RUNNING)
            
            # Notify via Mission's own centralized status module
            mission = self.mission_queue.get_current_mission()
            if mission and mission._centralized_status_mission:
                mission._centralized_status_mission.update({
                    "mission_id": ack_mission_id,
                    "mission_state": MissionStateAll.RUNNING.name,
                })
            
            # Note: No need to spawn _execute_mission_loop anymore
            # The continuous _mission_runner_loop will detect RUNNING state and execute
            logger.info(f"{LogIcons.RUN} Mission state set to RUNNING - runner loop will execute")
            return True
        except Exception as e:
            logger.error(
                f"{LogIcons.ERROR} Failed to start mission loop for ID '{ack_mission_id}': {e}, "
                f"trace: {traceback.format_exc()}"
            )
            return False
    
    
    # ══════════════════════════════════════════════════════════════════
    # §4. MISSION LOADING & VALIDATION
    # ══════════════════════════════════════════════════════════════════
    
    def _check_duplicate_mission(self, new_mission_id: str) -> bool:
        current_id = self.mission_queue.get_current_mission_id()
        if current_id and current_id == new_mission_id and self._is_mission_in_progress():
            logger.info(f"{LogIcons.SUCCESS} Mission '{new_mission_id}' is already running. Ignoring duplicate run request.")
            return True
        return False  


    
    # ══════════════════════════════════════════════════════════════════
    # §7. FC COMMUNICATION (MAVLink Senders)
    # ══════════════════════════════════════════════════════════════════
    
    async def _mavlink_heartbeat_loop(self):
        """Loop to send MAVLink heartbeat at 10Hz with lazy retry on failure."""
        logger.info(f"{LogIcons.RUN} MAVLink heartbeat loop started (10Hz)")
        consecutive_failures = 0
        max_backoff = 5.0  # Maximum backoff in seconds
        
        while True:
            try:
                success = self._send_leaf_heartbeat()
                if success:
                    if consecutive_failures > 0:
                        logger.info(f"{LogIcons.SUCCESS} MAVLink heartbeat resumed after {consecutive_failures} failures")
                    consecutive_failures = 0
                else:
                    consecutive_failures += 1
            except Exception as e:
                consecutive_failures += 1
                logger.error(f"{LogIcons.ERROR} Error sending MAVLink heartbeat: {e}")
            
            # Lazy retry: back off on consecutive failures
            if consecutive_failures > 0:
                backoff = min(0.1 * (2 ** consecutive_failures), max_backoff)
                if consecutive_failures % 10 == 1:  # Log every 10th failure to avoid spam
                    logger.warning(f"{LogIcons.WARNING} MAVLink heartbeat: {consecutive_failures} consecutive failures, backing off {backoff:.1f}s")
                await asyncio.sleep(backoff)
            else:
                await asyncio.sleep(1)  # 10Hz

    def _send_leaf_heartbeat(self) -> bool:
        """Send LEAF_MISSION_HEARTBEAT message.
        
        Returns:
            True if message was sent successfully, False otherwise.
        """
        mission_status = leafMAV.LEAF_MISSION_STATE_IDLE
        joystick_mode = leafMAV.ENABLED_ALWAYS
        mission_id_str = ""
        predefined_actions_status = leafMAV.NOT_STARTED

        # Get current status: prefer proposed_state (what we want) over current_state (confirmed)
        if self._distributed_mission_state:
             if self._distributed_mission_state.proposed_state is not None:
                 mission_status = self._distributed_mission_state.proposed_state.value
             else:
                 mission_status = self._distributed_mission_state.current_state.value

        # Get Mission details if active
        if self._has_active_mission():
             mission = self.mission_queue.get_current_mission()
             if mission:
                 mission_id_str = mission.mission_id
                 if mission.mission_config and hasattr(mission.mission_config, 'joystick_mode'):
                      # Map config joystick mode to MAVLink enum
                      try:
                          # Check if it's an Enum and get value, or use as is if already int/int-like
                          if hasattr(mission.mission_config.joystick_mode, 'value'):
                              joystick_mode = mission.mission_config.joystick_mode.value
                          else:
                              joystick_mode = int(mission.mission_config.joystick_mode)
                      except (ValueError, TypeError):
                          pass

        msg = leafMAV.MAVLink_leaf_mission_heartbeat_message(
            mission_status=mission_status,
            joystick_mode=joystick_mode,
            mission_id=mission_id_str.encode('ascii'),
            queue_count=len(self.mission_queue.items),
            predefined_actions_status=predefined_actions_status
        )
        
        if not self._mavlink_proxy:
            logger.warning(f"{LogIcons.WARNING} Cannot send LEAF_MISSION_HEARTBEAT: MAVLink proxy not available")
            return False
        
        self._mavlink_proxy.send("mav", msg)
        logger.info(f"{LogIcons.PUBLISH} LEAF_MISSION_HEARTBEAT: status={mission_status}, mission_id='{mission_id_str}', queue={len(self.mission_queue.items)}")
        
        return True

    def _send_state_to_fc(self, state: MissionStateAll, mission_id: str = None) -> bool:
        """
        Send mission state to FC using LEAF_SET_MISSION_STATE message.
        
        This is the unified state distribution function - all state changes
        go through here to the FC.
        
        Args:
            state: The MissionStateAll state to send
            mission_id: Optional mission ID (uses current if None)
            
        Returns:
            True if message was sent successfully
        """
        if mission_id is None:
            mission_id = self.mission_queue.get_current_mission_id()
        
        # Allow empty mission_id for IDLE/CANCELLED states (cleanup/reset/abort scenarios)
        if not mission_id and state not in [MissionStateAll.IDLE, MissionStateAll.CANCELLED]:
            logger.warning(f"{LogIcons.WARNING} Cannot send state to FC: no mission ID")
            return False
        
        # Use empty string for cleanup if no mission
        if not mission_id:
            mission_id = ""
        
        # Map MissionStateAll to leafMAV LEAF_MISSION_STATE enum value
        msg = leafMAV.MAVLink_leaf_set_mission_state_message(
            target_system=self._mavlink_proxy.target_system,
            state=state.value,  # MissionStateAll values match LEAF_MISSION_STATE
            mission_id=mission_id.encode("ascii")
        )
        return send_mavlink_message(
            self._mavlink_proxy, msg, 
            f"mission state {state.name} to FC for mission '{mission_id}'",
            MAVLinkConstants.MAVLINK_BURST_COUNT, MAVLinkConstants.MAVLINK_BURST_INTERVAL
        )
    
    def _send_abort_to_fc(self) -> bool:
        """
        Send abort (CANCELLED state) to FC for orphaned mission cleanup.
        
        This is used when we detect FC has a running mission but local state is IDLE.
        We send CANCELLED with empty mission_id to abort the orphaned mission.
        
        Returns:
            True if message was sent successfully
        """
        logger.warning(f"{LogIcons.CANCEL} Sending ABORT to FC to clean up orphaned mission")
        return self._send_state_to_fc(MissionStateAll.CANCELLED, mission_id="")
    
    def _send_arm_command(self, arm: bool = True) -> bool:
        """Send LEAF_DO_ARM_IDLE command to FC (msg 77017).
        
        Args:
            arm: True to arm/idle (enable=1), False to disarm (enable=0)
            
        Returns:
            True if message was sent successfully
        """
        if not self._mavlink_proxy:
            logger.warning(f"{LogIcons.WARNING} Cannot send arm command: MAVLink proxy unavailable")
            return False
        
        # LEAF_DO_ARM_IDLE (77017): enable=1 to arm/idle, enable=0 to disarm
        msg = leafMAV.MAVLink_leaf_do_arm_idle_message(
            target_system=self._mavlink_proxy.target_system,
            enable=1 if arm else 0
        )
        return send_mavlink_message(
            self._mavlink_proxy, msg,
            f"{'ARM_IDLE' if arm else 'DISARM'} command to FC",
            MAVLinkConstants.MAVLINK_BURST_COUNT, MAVLinkConstants.MAVLINK_BURST_INTERVAL
        )
    
    
    # ══════════════════════════════════════════════════════════════════
    # §5. MISSION EXECUTION FLOW
    # ══════════════════════════════════════════════════════════════════
    
    def start_mission(self, mission_id: str = None) -> bool:
        """
        Start mission execution (synchronous entry point for multi-endpoint access).
        
        This method can be called from any endpoint (MAVLink, HTTP, MQTT, Redis, etc.)
        to trigger mission execution. It prepares the mission and triggers the runner loop.
        
        If FC is in READY_TO_FLY state, it will automatically arm and wait for ARMED_IDLE.
        
        Args:
            mission_id: Optional specific mission ID to run. If None, runs next in queue.
            
        Returns:
            True if mission start was triggered, False if rejected.
        """
        # Reject if already in progress
        if self._is_mission_in_progress():
            logger.warning(f"{LogIcons.WARNING} Cannot start - mission already in progress")
            return False
        
        # Resolve target mission
        if mission_id is None or not mission_id.strip():
            mission_item = self.mission_queue.peek()
            if mission_item is None:
                logger.error(f"{LogIcons.ERROR} Queue is empty - no mission to start")
                return False
            mission_id = mission_item["id"]
        else:
            if self.mission_queue.find_by_id(mission_id) is None:
                logger.error(f"{LogIcons.ERROR} Mission not found in queue: {mission_id}")
                return False
        
        # Promote mission to front of queue
        if not self.mission_queue.promote_to_front(mission_id):
            logger.error(f"{LogIcons.ERROR} Failed to promote mission to front: {mission_id}")
            return False
        
        # Apply joystick mode configuration
        mission = self.mission_queue.get_current_mission()
        if mission and mission.mission_config:
            StatelessMissionFunctions.apply_joystick_mode(mission.mission_config, self._redis_proxy)
        
        # Start mission immediately - Takeoff step will handle FC arming if needed
        logger.info(f"{LogIcons.RUN} Starting mission: {mission_id}")
        self._distributed_mission_state.propose(MissionStateAll.RUNNING)
        return True
    
    async def _wait_for_arm_and_start(self, mission_id: str, timeout: float = 5.0):
        """Wait for FC to arm, then start mission. Returns mission to READY on timeout."""
        logger.info(f"{LogIcons.INFO} Waiting up to {timeout}s for FC to arm...")
        
        poll_interval = 0.2
        elapsed = 0.0
        
        while elapsed < timeout:
            fc_status = self._fc_status_provider.get_leaf_status()
            # Check if armed (ARMED_IDLE or ARMED)
            if fc_status in [leafMAV.LEAF_STATUS_ARMED_IDLE, leafMAV.LEAF_STATUS_ARMED]:
                logger.info(f"{LogIcons.SUCCESS} FC armed successfully, starting mission: {mission_id}")
                self._distributed_mission_state.propose(MissionStateAll.RUNNING)
                return
            
            await asyncio.sleep(poll_interval)
            elapsed += poll_interval
        
        # Timeout - arming failed
        logger.error(f"{LogIcons.ERROR} FC did not arm within {timeout}s, returning mission to READY state")
        self._distributed_mission_state.propose(MissionStateAll.READY)
    
    async def _delayed_auto_start(self, mission_id: str):
        """
        Auto-start with IDLE delay sequence:
        1. Send IDLE state to FC
        2. Wait 5 seconds
        3. Start mission (send RUNNING state)
        """
        try:
            # Step 1: Send IDLE first
            logger.info(f"{LogIcons.INFO} Sending IDLE before auto-start for mission '{mission_id}'")
            self._distributed_mission_state.propose(MissionStateAll.IDLE)
            
            # Step 2: Wait 5 seconds
            logger.info(f"{LogIcons.INFO} Waiting 5 seconds before starting mission '{mission_id}'...")
            await asyncio.sleep(5.0)
            
            # Step 3: Start mission
            logger.info(f"{LogIcons.RUN} Starting mission after delay: {mission_id}")
            self.start_mission(mission_id)
            
        except asyncio.CancelledError:
            logger.warning(f"{LogIcons.WARNING} Auto-start cancelled for mission '{mission_id}'")
        except Exception as e:
            logger.error(f"{LogIcons.ERROR} Auto-start error for mission '{mission_id}': {e}")
    
    async def _mission_runner_loop(self):
        """
        Continuous mission execution loop - runs forever until shutdown.
        
        This single long-running coroutine handles all mission execution.
        It reacts to state changes rather than spawning new coroutines per mission.
        Runs at the configured clock rate (default 50Hz) when executing.
        """
        logger.info(f"{LogIcons.RUN} Mission runner loop starting...")
        
        while self._is_runner_active:
            try:
                # Get current distributed state (source of truth with FC)
                current_state = self._distributed_mission_state.current_state
                mission = self.mission_queue.get_current_mission()
                
                if current_state == MissionStateAll.RUNNING and mission:
                    # Execute one step iteration at clock rate
                    self.mission_clock.tick()
                    step_completed = mission.run_step()
                    if step_completed:
                        status = mission.gen_dict_status()
                        await self.publish_status_update(status)
                    await self.mission_clock.tock(blocking=False)
                    
                    # Check if mission ended (run_step may have changed state)
                    mission_state = mission.mission_status.get_state()
                    if mission_state.is_completed():
                        logger.info(f"{LogIcons.SUCCESS} Mission completed with state: {mission_state.name}")
                        self._mission_completion(success=(mission_state == MissionStateAll.COMPLETED))
                        
                elif current_state in [MissionStateAll.PAUSED_MID_STEP, MissionStateAll.PAUSED_BETWEEN_STEPS]:
                    # Paused - wait for resume
                    await asyncio.sleep(0.1)
                    
                elif current_state == MissionStateAll.SCHEDULED_PAUSE and mission:
                    # Pause is scheduled, continue until step completes
                    self.mission_clock.tick()
                    step_completed = mission.run_step()
                    if step_completed:
                        status = mission.gen_dict_status()
                        await self.publish_status_update(status)
                    await self.mission_clock.tock(blocking=False)
                    
                else:
                    # IDLE, READY, COMPLETED, FAILED, SAFETY - wait for state change
                    # Handle CANCELLED: reset to IDLE and check for next mission
                    if current_state == MissionStateAll.CANCELLED:
                        self._distributed_mission_state.propose(MissionStateAll.IDLE)
                        logger.info(f"{LogIcons.INFO} Proposing state reset to IDLE after CANCELLED")
                        # Check if there's another mission in queue - if so, set to READY
                        if not self.mission_queue.is_empty():
                            self._distributed_mission_state.propose(MissionStateAll.READY)
                            logger.info(f"{LogIcons.INFO} Mission in queue detected - proposing state to READY")
                    await asyncio.sleep(0.1)
                    
            except asyncio.CancelledError:
                logger.info(f"{LogIcons.INFO} Mission runner loop cancelled")
                break
            except Exception as e:
                logger.error(f"{LogIcons.ERROR} Mission runner error: {e}")
                logger.error(traceback.format_exc())
                # Try to recover - mark mission as failed if there is one
                mission = self.mission_queue.get_current_mission()
                if mission:
                    self._mission_completion(success=False)
                await asyncio.sleep(1.0)  # Backoff on error
        
        logger.info(f"{LogIcons.INFO} Mission runner loop exited")

    
    def _validate_and_enqueue_mission(self, mission_data: dict) -> tuple[bool, str, Optional[str]]:
        """
        Validate, create mission, and enqueue mission.
        
        Architecture:
        - MissionPlan has only 'name' (with UUID suffix appended in constructor)
        - Mission generates its own unique 'id' when loading the plan
        - Mission ID is used for queue tracking and FC communication
        - Mission name (from plan) is used for duplicate detection
        
        This function creates the Mission instance immediately and stores it in the queue.
        The mission is created without registering handlers - the plugin manages all handlers.
        
        Args:
            mission_data: Already-validated mission plan dict (from MissionPlanDTO)
        
        Returns:
            Tuple of (success: bool, message: str, error: Optional[str])
        """
        mission_config = None
        mission_executor = None

        def parse_config()-> bool:
            nonlocal mission_config
            
            try:
                mission_config = MissionConfig.from_dict(mission_data.get("config", {}))
            except Exception as exc:
                logger.error(f"{LogIcons.ERROR} Mission config parsing failed: {exc}")
                raise ValueError(f"Invalid mission configuration: {exc}")
            
            return True
        
        def create_mission() -> bool:
            """Create mission without registering handlers. Mission generates its own ID."""
            nonlocal mission_executor
            
            try:
                mission_executor = Mission(
                    mav_proxy=self._mavlink_proxy,
                    redis_proxy=self._redis_proxy,
                    data=mission_data,
                    fc_status_provider=self._fc_status_provider,
                    setpoint_offset=self.setpoint_offset,
                    status_manager=self._centralized_status_manager,  # Pass manager to Mission
                )
                
                result = mission_executor.load_plan()
                if not result:
                    logger.error(f"{LogIcons.ERROR} Mission failed to load.")
                    return False
                
                # Mission now has its own unique ID generated in load_plan()
                logger.info(f"{LogIcons.SUCCESS} Created mission '{mission_executor.mission_name}' (ID: {mission_executor.mission_id})")
                logger.info(f"{LogIcons.SUCCESS} Mission '{mission_executor.mission_name}' loaded and validated")
                return True
                
            except Exception as exc:
                logger.error(f"{LogIcons.ERROR} Mission creation failed: {exc}")
                logger.error(traceback.format_exc())
                return False

        def check_mission_in_progress() -> tuple[bool, Optional[str]]:
            """Check if mission is in progress and handle based on MissionLoadBehavior."""
            if not self._is_mission_in_progress():
                return True, None
            
            behavior = mission_config.mission_load_behavior
            
            if behavior == MissionLoadBehavior.ERROR_IF_MISSION_IN_PROGRESS:
                return False, "Cannot load mission: another mission is currently in progress"
            elif behavior == MissionLoadBehavior.REPLACE_IF_MISSION_IN_PROGRESS:
                logger.warning(f"{LogIcons.WARNING} Replacing current mission with new mission '{mission_executor.mission_id}'")
                self.abort()
                return True, None
            else:  # QUEUE_IF_MISSION_IN_PROGRESS (default)
                logger.info(f"{LogIcons.RUN} Queueing mission '{mission_executor.mission_id}' - another mission in progress")
                return True, None

        def enqueue_mission() -> bool:
            """Enqueue the pre-created and validated mission."""
            
            enqueue_success, error_msg = self.mission_queue.enqueue(
                id=mission_executor.mission_id,
                data=mission_executor,
                allow_duplicate_names=mission_config.allow_duplicate_names,
                mission_name=mission_executor.mission_name  # Mission name for duplicate checking
            )
            if not enqueue_success:
                logger.error(f"{LogIcons.ERROR} Failed to enqueue: {error_msg}")
                return False
            
            # Note: Queue update is now handled by MissionQueue itself
            
            # Auto-start if config specifies AUTOSTART_ON_LOAD_IMMEDIATELY
            if mission_config.auto_start_behavior == AutoStartBehavior.AUTOSTART_ON_LOAD_IMMEDIATELY:
                logger.info(f"{LogIcons.RUN} Auto-starting mission '{mission_executor.mission_id}'...")
                asyncio.run_coroutine_threadsafe(
                    self._delayed_auto_start(mission_executor.mission_id),
                    self._event_loop
                )
            else:
                # If not auto-starting, and no other mission is running, set to READY
                if not self._is_mission_in_progress():
                    self._distributed_mission_state.propose(MissionStateAll.READY)
                    logger.info(f"{LogIcons.INFO} Mission enqueued - state set to READY")
            
            return True

        try:
            # Parse mission configuration
            if not parse_config():
                return (False, "Mission config parsing failed", "Invalid mission configuration")
            
            if not create_mission():
                return (False, "Mission creation failed", "Failed to create or load mission")
            
            can_load, load_error = check_mission_in_progress()
            if not can_load:
                return (False, load_error, load_error)
            
            # Enqueue mission
            if not enqueue_mission():
                return (False, "Failed to enqueue mission", "Queue is full or duplicate ID exists")
            
            logger.info(f"{LogIcons.SUCCESS} Mission '{mission_executor.mission_id}' accepted and enqueued")
            return (True, f"Mission '{mission_executor.mission_id}' accepted and enqueued", None)

        except Exception as exc:
            logger.warning(f"{LogIcons.WARNING} Invalid mission payload: {exc}")
            return (False, "Invalid mission payload", str(exc))

    def _mission_completion(self, success = True):
        """
        Handle mission completion - cleanup mission and trigger success/failure handlers.
        
        This function is called when a mission finishes (successfully or not) and:
        1. Logs completion status
        2. Delegates to success/failure handlers (which manage queue behavior)
        3. Cleans up mission and clears mission ID
        4. Sends mission done message to flight controller
        
        The success/failure handlers determine what happens next based on
        mission configuration (idle, load next, retry, etc.).
        
        Args:
            success: True if mission completed successfully, False if it failed
        
        Note:
            Always deletes mission to ensure fresh state for next mission run.
        """
        completed_mission_id = self.mission_queue.get_current_mission_id()
        
        # Notify via Mission's own centralized status module
        mission = self.mission_queue.get_current_mission()
        final_state = MissionStateAll.COMPLETED.name if success else MissionStateAll.FAILED.name
        if mission and mission._centralized_status_mission:
            mission._centralized_status_mission.update({
                "mission_id": completed_mission_id,
                "mission_state": final_state,
            })
        
        # Signal completion via distributed state FIRST (while mission is still in queue)
        final_state = MissionStateAll.COMPLETED if success else MissionStateAll.CANCELLED
        self._distributed_mission_state.propose(final_state)
        
        # Send IDLE immediately after terminal state (while mission still in queue)
        logger.info(f"{LogIcons.INFO} Sending IDLE state to FC after {final_state.name}")
        self._send_state_to_fc(MissionStateAll.IDLE, completed_mission_id)
        
        # Now handle mission cleanup (which dequeues it)
        if not success:
            logger.error(f"{LogIcons.ERROR} Mission failed (ID: '{completed_mission_id}')")
            self._handle_mission_failure(completed_mission_id)
        else:
            logger.info(f"{LogIcons.SUCCESS} Mission completed successfully (ID: '{completed_mission_id}')")
            self._handle_mission_success(completed_mission_id)
    
    def _handle_next_mission_action(self, result: dict, context: str) -> None:
        """
        Handle the next mission action based on queue decision.
        
        Args:
            result: Result dictionary from queue with 'action' and optional 'next_mission_id'
            context: Context for logging (e.g., 'after success', 'after failure')
        """
        action = result.get('action')
        next_mission_id = result.get('next_mission_id')
        
        if action in ['load_next', 'retry_mission', 'restart_mission'] and next_mission_id:
            action_label = {
                'load_next': 'Loading next mission',
                'retry_mission': 'Retrying mission',
                'restart_mission': 'Restarting mission'
            }.get(action, f'Executing {action}')
            
            logger.info(f"{LogIcons.RUN} {action_label} {context}: '{next_mission_id}'")
            self.start_mission(next_mission_id)
        # 'idle' action requires no further steps
    
    def _handle_mission_failure(self, mission_id: str):
        """
        Handle failed mission by delegating to queue and acting on instructions.
        
        Delegates to mission queue to determine next action based on the mission's
        unsuccessful_completion_behavior configuration. Possible actions:
        - 'idle': Do nothing, stop execution
        - 'load_next': Start next mission in queue
        - 'retry_mission': Retry the failed mission
        
        Args:
            mission_id: ID of the mission that failed
        """
        result = self.mission_queue.handle_mission_failure()
        self._handle_next_mission_action(result, 'after failure')
    
    def _handle_mission_success(self, mission_id: str):
        """
        Handle successful mission completion by delegating to queue and acting on instructions.
        
        Delegates to mission queue to determine next action based on the mission's
        successful_completion_behavior configuration. Possible actions:
        - 'idle': Do nothing, stop execution
        - 'load_next': Start next mission in queue
        - 'restart_mission': Restart the same mission (for loops)
        
        Args:
            mission_id: ID of the mission that completed successfully
        """
        result = self.mission_queue.handle_mission_success()
        self._handle_next_mission_action(result, 'after success')

    
    # ══════════════════════════════════════════════════════════════════
    # §8. STATUS PUBLISHING
    # ══════════════════════════════════════════════════════════════════
    
    async def publish_status_update(self, status: dict):
        if "step_completed" not in status:
            status["step_completed"] = True
        await self.publish_status_update_httpx(status)
        self.publish_status_update_redis(status)
    

    
    # ══════════════════════════════════════════════════════════════════
    # §6. MISSION CONTROL OPERATIONS
    # ══════════════════════════════════════════════════════════════════

    def pause(self) -> bool:
        """Pause the current mission and notify flight controller."""
        if not self._is_mission_in_progress():
            logger.warning(f"{LogIcons.WARNING} No running plan available to pause, trying anyway: ...")
            return False
        
        mission = self.mission_queue.get_current_mission()
        mission_id = self.mission_queue.get_current_mission_id()
        
        if mission is None:
            logger.warning(f"{LogIcons.WARNING} No mission available to pause")
            return False
        
        try:
            result = mission.pause()
            logger.info(f"{LogIcons.SUCCESS} Mission paused for '{mission_id}'")
            
            if result and mission_id:
                self._distributed_mission_state.propose(MissionStateAll.PAUSED_MID_STEP)
            
            return True
        except Exception as e:
            logger.error(f"{LogIcons.ERROR} Failed to pause mission: {e}, trace: {traceback.format_exc()}")
            return False

    def resume(self) -> bool:
        """Resume the current mission and notify flight controller."""
        mission = self.mission_queue.get_current_mission()
        if mission is None:
             logger.warning(f"{LogIcons.WARNING} No mission available to resume")
             return False
             
        if not mission.mission_status.is_currently_paused():
            logger.warning(f"{LogIcons.WARNING} Mission is not paused (State: {mission.mission_status.get_state().name}), cannot resume.")
            return False
        mission_id = self.mission_queue.get_current_mission_id()
        
        try:
            result = mission.resume()
            logger.info(f"{LogIcons.SUCCESS} Mission resumed for '{mission_id}'")
            
            if result and mission_id:
                self._distributed_mission_state.propose(MissionStateAll.RUNNING)
            
            return True
        except Exception as e:
            logger.error(f"{LogIcons.ERROR} Failed to resume mission: {e}")
            return False

    def abort(self) -> bool:
        """Abort the currently running mission."""
        current_state = self._distributed_mission_state.current_state
        
        if not self._has_active_mission():
            logger.warning(f"{LogIcons.WARNING} No active mission to abort")
            # Allow abort on terminal states to reset to IDLE
            if current_state in [MissionStateAll.COMPLETED, MissionStateAll.FAILED, MissionStateAll.CANCELLED]:
                logger.info(f"{LogIcons.INFO} Mission in terminal state {current_state.name}, transitioning to IDLE")
                self._distributed_mission_state.propose(MissionStateAll.IDLE)
                return True
            return False
        
        aborted_mission_id = self.mission_queue.get_current_mission_id()
        mission = self.mission_queue.get_current_mission()
        current_state = self._distributed_mission_state.current_state
        
        # If already in terminal state, just transition to IDLE
        
        try:
            # 1. Update Distributed State (send to FC) BEFORE dequeuing
            # This ensures we use the correct mission ID for the FC command
            self._distributed_mission_state.propose(MissionStateAll.CANCELLED)

            if mission is not None:
                logger.warning(f"{LogIcons.CANCEL} Aborting mission '{aborted_mission_id}'")
                self.mission_queue.handle_mission_failure() #INCLUDES DEQUEUE
                
                try:
                    result = mission.abort()
                    logger.info(f"{LogIcons.SUCCESS} Mission aborted for '{aborted_mission_id}'")
                except Exception as e:
                    logger.error(f"{LogIcons.ERROR} Error aborting mission: {e}")
            else:
                logger.warning(f"{LogIcons.WARNING} No active mission (mission ID: '{aborted_mission_id}')")
        
        except Exception as e:
            logger.error(f"{LogIcons.ERROR} Failed to abort mission '{aborted_mission_id}': {e}")
            # Ensure we still dequeue on error to prevent stuck state
            self.mission_queue.dequeue()
            return False
        
        return True

    def land_in_place(self) -> bool:
        """
        Send land-in-place command to the flight controller.
        
        Requirements:
        - Drone must be in HOVERING or MOVING state
        - Mission state must be IDLE or READY (no active mission)
        
        Returns:
            True if land command was sent successfully, False otherwise
        """
        # Check if FC is in flying state
        drone_state = self._fc_status_provider.get_drone_state()
        if drone_state not in [DroneState.HOVERING, DroneState.MOVING]:
            logger.warning(
                f"{LogIcons.WARNING} Cannot land in place: Drone state is {drone_state.value}, "
                f"must be hovering or moving"
            )
            return False
        
        # Check if mission is idle
        current_state = self._distributed_mission_state.current_state
        if current_state not in [MissionStateAll.IDLE, MissionStateAll.READY, MissionStateAll.CANCELLED, MissionStateAll.COMPLETED, MissionStateAll.FAILED]:
            logger.warning(
                f"{LogIcons.WARNING} Cannot land in place: Mission state is {current_state.name}, "
                f"must be IDLE or READY"
            )
            return False
        
        # Send land command to FC
        try:
            msg = leafMAV.MAVLink_leaf_do_land_message(
                target_system=self._mavlink_proxy.target_system,
            )
            success = send_mavlink_message(
                self._mavlink_proxy, msg,
                "land-in-place command to FC",
                MAVLinkConstants.MAVLINK_BURST_COUNT,
                MAVLinkConstants.MAVLINK_BURST_INTERVAL
            )
            
            if success:
                logger.info(f"{LogIcons.SUCCESS} Land-in-place command sent to FC")
                return True
            else:
                logger.error(f"{LogIcons.ERROR} Failed to send land-in-place command")
                return False
                
        except Exception as e:
            logger.error(f"{LogIcons.ERROR} Error sending land command: {e}")
            return False

        
    
    def return_to_launch(self):
        # Create RTL mission
        rtl_mission_dict = self._create_rtl_mission()
        if rtl_mission_dict is None:
            error_msg = "Failed to create RTL mission: Home position not available"
            logger.error(f"{LogIcons.ERROR} {error_msg}")
            return {
                "status": "error",
                "message": error_msg,
                "error": None
            }
        
        logger.info(f"{LogIcons.SUCCESS} RTL mission created, loading...")
        success, message, error = self._validate_and_enqueue_mission(rtl_mission_dict)
        
        if success:
            # Trigger start explicitly
            self.start_mission()
            message = "RTL mission loaded and started"
        
        if success:
            logger.info(f"{LogIcons.SUCCESS} RTL mission loaded and started: {message}")
            return {
                "status": "success",
                "message": message,
                "error": None
            }
        else:
            logger.error(f"{LogIcons.ERROR} RTL mission failed: {error}")
            return {
                "status": "error",
                "message": message,
                "error": error
            }




    # ══════════════════════════════════════════════════════════════════
    # §9. HTTP WEB API ENDPOINTS
    # ══════════════════════════════════════════════════════════════════

    @http_action(
        method="POST",
        path="/mission/plan",
        description="Receives a mission plan and runs it in the background",
        summary="Execute Mission Plan",
        tags=["mission"]
    )
    async def receive_mission(self, data: MissionPlanDTO):
        try:
            mission_dict = data.model_dump(by_alias=True)
            success, message, error = self._validate_and_enqueue_mission(mission_dict)
        except Exception as exc:
            logger.error(f"{LogIcons.ERROR} Failed to process mission: {exc}")
            success, message, error = False, "Mission processing failed", str(exc)
        return {"status": f"{'SUCCESS' if success else 'ERROR'}: {message}{'' if success else f', error: {error}'}"}
    
    @http_action(
        method="POST",
        path="/mission/subscribe_to_progress_updates",
        description="Receives an address where mission progress updates will be posted"
    )
    async def subscribe_to_progress_updates(self, data: ProgressUpdateSubscription):
        self.subscriber_address = data.address.rstrip("/")  # remove trailing slash if present
        logger.info(f"{LogIcons.SUCCESS} Subscribed to mission progress updates at: {self.subscriber_address}")
        return {"status": f"{LogIcons.SUCCESS} Subscribed"}
    
    # # Not used in the current implementation, but can be used to set a safe return waypoint request address
    # @http_action(
    #     method="POST",
    #     path="/mission/set_safe_return_plan_request_address",
    #     description="Sets the address for safe return plan requests"
    # )
    # async def set_safe_return_plan_request_address(self, data: SafeReturnPlanRequestAddress):
    #     self.safe_return_plan_request_address = data.address.rstrip("/")  # remove trailing slash if present
    #     logger.info(f"{LogIcons.SUCCESS} Set safe return plan request address to: {self.safe_return_plan_request_address}")
    #     return {"status": f"{LogIcons.SUCCESS} Safe return plan request address set"}

    # # Not used in the current implementation, but can be used to handle safe return plan requests
    # @http_action(
    #     method="GET",
    #     path="/mission/safe_return_plan_request",
    #     description="Receives a safe return plan request and feeds it to the mission planner"
    # )
    # async def safe_return_plan_request(self):
    #     if not self.safe_return_plan_request_address:
    #         logger.warning(f"{LogIcons.WARNING} No safe return plan request address set")
    #         return {"status": f"{LogIcons.WARNING} No safe return plan request address set", "error": "Address not initialized"}
    #     # ToDo: implement safe return plan request
    #     pass

    @http_action(
        method="POST",
        path="/mission/pause",
        description="Pauses the currently running mission"
    )
    async def pause_mission(self):
        if self.pause():
            logger.info(f"{LogIcons.PAUSE} Mission paused successfully")
            return {"status": f"{LogIcons.PAUSE} Mission pause command received successfully!"}
        else:
            logger.error(f"{LogIcons.ERROR} Failed to pause mission")
            return {"status": f"{LogIcons.ERROR} Failed to pause mission", "error": "Unable to pause mission"}

    @http_action(
        method="POST",
        path="/mission/resume",
        description="Resumes a paused mission"
    )
    async def resume_mission(self):
        if self.resume():
            logger.info(f"{LogIcons.RESUME} Mission resumed successfully")
            return {"status": f"{LogIcons.RESUME} Mission resume command received successfully!"}
        else:
            logger.error(f"{LogIcons.ERROR} Failed to resume mission")
            return {"status": f"{LogIcons.ERROR} Failed to resume mission", "error": "Unable to resume mission"}

    @http_action(
        method="POST",
        path="/mission/abort",
        description="Aborts the currently running mission"
    )
    async def abort_mission(self):
        self.abort()
        return {"status": f"{LogIcons.CANCEL} Mission abort command received successfully!"}
    
    @http_action(
        method="POST",
        path="/mission/land",
        description="Land in place - Commands the drone to land at current position",
        summary="Land in Place",
        tags=["mission"]
    )
    async def land_mission(self):
        """Command drone to land at current position.
        
        Requirements:
        - Drone must be flying (hovering or moving)
        - No active mission (mission state must be IDLE or READY)
        """
        try:
            logger.info(f"{LogIcons.RUN} HTTP land command received")
            success = self.land_in_place()
            
            if success:
                return {
                    "status": "success",
                    "message": "Land-in-place command sent successfully"
                }
            else:
                return {
                    "status": "error",
                    "message": "Failed to send land command - check drone state and mission status"
                }
                
        except Exception as exc:
            logger.error(f"{LogIcons.ERROR} Land HTTP handler error: {exc}")
            return {
                "status": "error",
                "message": "Land command failed",
                "error": str(exc)
            }
    
    @http_action(
        method="POST",
        path="/mission/rtl",
        description="Return to Launch - Creates and executes RTL mission to home position",
        summary="Return to Launch (RTL)",
        tags=["mission"]
    )
    async def rtl_mission(self):
        """Create and execute an RTL (Return to Launch) mission.
        
        The RTL mission will:
        1. Navigate to home position at safe altitude (max of 2m or current altitude)
        2. Land at home position
        
        Requires home position to be available from flight controller.
        """
        try:
            logger.info(f"{LogIcons.RUN} HTTP RTL command received")
            self.return_to_launch()
            return {"status": f"{LogIcons.SUCCESS} RTL mission loaded and started"}
                
        except Exception as exc:
            logger.error(f"{LogIcons.ERROR} RTL HTTP handler error: {exc}")
            logger.error(traceback.format_exc())
            return {
                "status": "error",
                "message": "RTL mission failed",
                "error": str(exc)
            }
    
    @http_action(
        method="POST",
        path="/mission/goto",
        description="Go to position - Creates and executes goto mission to specified coordinates",
        summary="Go to Position",
        tags=["mission"]
    )
    async def goto_position(self, data: GotoRequest):
        """Create and execute a goto mission to specified position.
        
        Supports three coordinate systems:
        - GPS: latitude/longitude/altitude (MSL)
        - Local: North/East/Down (NED coordinates)
        - Relative: offset from current position
        
        Altitude is optional - if not provided, maintains current altitude.
        Only works when drone is flying.
        """
        try:
            logger.info(f"{LogIcons.RUN} HTTP goto command received: {data.position_type}")
            
            # Create goto mission
            goto_mission_dict = self._create_goto_mission(data)
            
            if goto_mission_dict is None:
                error_msg = "Failed to create goto mission: Check drone state and position validity"
                logger.error(f"{LogIcons.ERROR} {error_msg}")
                return {
                    "status": "error",
                    "message": error_msg
                }
            
            # Load and start the goto mission
            logger.info(f"{LogIcons.SUCCESS} Goto mission created, loading...")
            success, message, error = self._validate_and_enqueue_mission(goto_mission_dict)
            
            if success:
                logger.info(f"{LogIcons.SUCCESS} Goto mission loaded and started: {message}")
                return {
                    "status": "success",
                    "message": message,
                    "position_type": data.position_type,
                    "target": {"x": data.x, "y": data.y, "z": data.z}
                }
            else:
                logger.error(f"{LogIcons.ERROR} Goto mission failed: {error}")
                return {
                    "status": "error",
                    "message": message,
                    "error": error
                }
                
        except Exception as exc:
            logger.error(f"{LogIcons.ERROR} Goto HTTP handler error: {exc}")
            logger.error(traceback.format_exc())
            return {
                "status": "error",
                "message": "Goto mission failed",
                "error": str(exc)
            }

    @http_action(
        method="POST",
        path="/mission/joystick_mode",
        description="Set joystick mode for manual control during missions",
        summary="Set Joystick Mode",
        tags=["mission"]
    )
    async def set_joystick_mode(self, data: JoystickModeRequest):
        """Set joystick mode for manual control during missions.
        
        Modes:
        - DISABLED: Joystick control is disabled
        - ENABLED: Joystick control is always enabled
        - ENABLED_ON_PAUSE: Joystick control is enabled only when mission is paused
        """
        if self._redis_proxy is None:
            logger.error(f"{LogIcons.ERROR} Redis proxy not available - cannot set joystick mode")
            return {"status": "error", "message": "Redis proxy not available"}
        
        try:
            joystick_mode = JoystickMode[data.mode]
            
            from petal_leafsdk.mission import StatelessMissionFunctions
            from leafsdk.core.mission.mission_plan import MissionConfig
            
            temp_config = MissionConfig(joystick_mode=joystick_mode)
            StatelessMissionFunctions.apply_joystick_mode(temp_config, self._redis_proxy)
            
            logger.info(f"{LogIcons.SUCCESS} Joystick mode set to {data.mode}")
            return {
                "status": "success",
                "message": f"Joystick mode set to {data.mode}",
                "mode": data.mode
            }
        except KeyError:
            logger.error(f"{LogIcons.ERROR} Invalid joystick mode: {data.mode}")
            return {
                "status": "error",
                "message": f"Invalid joystick mode: {data.mode}. Valid modes: DISABLED, ENABLED_ALWAYS, ENABLED_ON_PAUSE"
            }
        except Exception as e:
            logger.error(f"{LogIcons.ERROR} Failed to set joystick mode: {e}")
            return {"status": "error", "message": str(e)}

    @http_action(
        method="POST",
        path="/mission/clear",
        description="Clear mission queue and reset mission to initial state",
        summary="Clear All Missions",
        tags=["mission"]
    )
    async def clear_missions(self):
        """Clear mission queue and reset to initial state."""
        try:
            if self._has_active_mission():
                logger.info(f"{LogIcons.CANCEL} Aborting current mission before clearing queue")
                self.abort()
            
            # Clear main queue
            cleared_count = len(self.mission_queue.items)
            self.mission_queue.items.clear()
            logger.info(f"{LogIcons.SUCCESS} Cleared {cleared_count} missions from main queue")
            
            # Optionally clear previous missions queue
            previous_count = len(self.previous_missions.items)
            self.previous_missions.items.clear()
            logger.info(f"{LogIcons.SUCCESS} Cleared {previous_count} previous missions")
            
            logger.info(f"{LogIcons.SUCCESS} System reset to initial state")
            return {
                "status": "success",
                "message": "Mission queue cleared",
                "cleared": {
                    "main_queue": cleared_count,
                    "previous_missions": previous_count
                }
            }
            
        except Exception as e:
            logger.error(f"{LogIcons.ERROR} Error clearing missions: {e}")
            return {
                "status": "error",
                "message": f"Failed to clear missions: {str(e)}"
            }

    @http_action(
        method="GET",
        path="/mission/queue",
        description="Get list of all missions in the queue",
        summary="List Queued Missions",
        tags=["mission"]
    )
    async def list_mission_queue(self):
        """Get list of all missions currently in the queue."""
        try:
            # Get missions from main queue
            main_queue_missions = []
            for i, item in enumerate(self.mission_queue.items):
                mission_info = {
                    "position": i + 1,
                    "id": item["id"],
                    "is_current": i == 0 and self._has_active_mission(),
                }
                # Extract info from mission if available
                try:
                    mission = item["data"]
                    if isinstance(mission, Mission):
                        # Get mission plan info from mission
                        if hasattr(mission, 'plan') and mission.plan:
                            mission_info["node_count"] = mission.plan._graph.number_of_nodes()
                        if hasattr(mission, 'mission_config') and mission.mission_config:
                            mission_info["config"] = mission.mission_config.to_dict()
                except Exception:
                    pass
                main_queue_missions.append(mission_info)
            
            # Get previous missions
            previous_missions_list = []
            for i, item in enumerate(self.previous_missions.items):
                previous_missions_list.append({
                    "position": i + 1,
                    "id": item["id"],
                })
            
            return {
                "status": "success",
                "queue": {
                    "main": {
                        "count": len(main_queue_missions),
                        "capacity": self.mission_queue.max_size,
                        "missions": main_queue_missions
                    },
                    "previous": {
                        "count": len(previous_missions_list),
                        "capacity": self.previous_missions.max_size,
                        "missions": previous_missions_list
                    }
                },
                "statistics": {
                    "total_enqueued": self.mission_queue._enqueue_count,
                    "total_dequeued": self.mission_queue._dequeue_count,
                    "peak_size": self.mission_queue._peak_size
                }
            }
            
        except Exception as e:
            logger.error(f"{LogIcons.ERROR} Error listing mission queue: {e}")
            return {
                "status": "error",
                "message": f"Failed to list mission queue: {str(e)}"
            }

    @http_action(
        method="GET",
        path="/fc/status",
        description="Get current Flight Controller status information",
        summary="Get FC Status",
        tags=["fc"]
    )
    async def get_fc_status_info(self):
        """Get comprehensive FC status information."""
        try:
            drone_state = self._fc_status_provider.get_drone_state()
            return {
                "status": "success",
                "fc_status": {
                    "drone_state": {
                        "value": drone_state.value,
                        "name": drone_state.name,
                        "flying": self._fc_status_provider.is_drone_flying(),
                        "safe_to_arm": self._fc_status_provider.is_drone_safe_to_arm(),
                        "ready_for_mission": self._fc_status_provider.is_drone_ready_for_mission(),
                    },
                    "leaf_status": {
                        "value": self._fc_status_provider.get_leaf_status(),
                        "name": self._fc_status_provider.get_leaf_status_name(),
                    },
                    "leaf_mission_status": {
                        "value": self._fc_status_provider.get_leaf_mission_status(),
                        "name": self._fc_status_provider.get_leaf_mission_status_name(),
                    },
                    "leaf_mode": {
                        "value": self._fc_status_provider.get_leaf_mode(),
                        "name": self._fc_status_provider.get_leaf_mode_name(),
                    },
                    "armed": self._fc_status_provider.is_fc_armed(),
                    "heartbeat": {
                        "last_received": self._fc_status_provider._last_heartbeat_time,
                        "age_seconds": self._fc_status_provider.get_heartbeat_age(),
                        "connected": self._fc_status_provider.is_fc_connected(),
                    },
                    "position": {
                        "home_position": self._fc_status_provider.get_home_position(),
                        "local_position_ned": {
                            **self._fc_status_provider.get_local_position_ned(),
                            "last_updated": self._fc_status_provider._last_local_position_time,
                            "age_seconds": time.time() - self._fc_status_provider._last_local_position_time if self._fc_status_provider._last_local_position_time > 0 else None,
                            "note": "Current vehicle position in local NED frame (from LOCAL_POSITION_NED message)",
                        },
                        "gps_origin": {
                            **(self._fc_status_provider.get_gps_origin_dict() or {}),
                            "note": "Origin of local NED frame (0,0,0 local = this GPS coordinate). Can be from GPS_GLOBAL_ORIGIN message or calculated from HOME_POSITION.",
                        } if self._fc_status_provider.has_gps_origin() else None,
                        "gps_from_local": self._fc_status_provider.get_gps_from_local_position(),
                    }
                }
            }
        except Exception as e:
            logger.error(f"{LogIcons.ERROR} Error getting FC status: {e}")
            return {
                "status": "error",
                "message": f"Failed to get FC status: {str(e)}"
            }

    async def publish_status_update_httpx(self, status: dict):
        if self.subscriber_address:
            try:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    await client.post(
                        self.subscriber_address,
                        json=status,
                        headers={"Content-Type": "application/json"},
                    )
            except Exception as e:
                logger.warning(f"{LogIcons.WARNING} Failed to report progress: {e}")



    
    # ══════════════════════════════════════════════════════════════════
    # §10. REDIS COMMAND HANDLERS
    # ══════════════════════════════════════════════════════════════════

    def _handle_redis_command_message(self, channel: str, data: str):
        try:
            cmd = RedisCommandPayload.model_validate_json(data)
        except Exception as exc:
            logger.warning(f"{LogIcons.WARNING} Invalid QGC command payload: {exc}")
            return False

        if cmd.command == "mission.plan":
            if cmd.payload is None:
                self._publish_redis_ack(cmd.message_id, cmd.command, status="error", error="Mission payload missing")
                return False

            try:
                asyncio.run_coroutine_threadsafe(
                    self._handle_redis_mission_plan_command(cmd.message_id, cmd.payload),
                    self._event_loop,
                )
            except RuntimeError as exc:
                logger.error(f"{LogIcons.ERROR} Failed to schedule mission plan handler: {exc}")
                self._publish_redis_ack(
                    cmd.message_id,
                    cmd.command,
                    status="error",
                    error="Mission handler unavailable",
                )
        else:
            logger.info(f"{LogIcons.RUN} Ignoring unsupported Redis command: {cmd.command}")

    async def _handle_redis_mission_plan_command(self, message_id: str, mission_graph: Dict[str, Any]):
        """Handle mission plan command from Redis with validation."""
        try:
            validated_mission = MissionPlanDTO.model_validate(mission_graph)
            success, message, error = self._validate_and_enqueue_mission(validated_mission.model_dump(by_alias=True))
        except Exception as exc:
            logger.error(f"{LogIcons.ERROR} Mission plan validation failed: {exc}")
            success, message, error = False, "Mission validation failed", str(exc)
        
        self._publish_redis_ack(
            message_id,
            "mission.plan",
            status="success" if success else "error",
            result=message,
            error=error,
        )
        return {f"{'success' if success else 'error'}: {message} {'' if success else f', error: {error}'}"}

    def _publish_redis_ack(
        self,
        message_id: Optional[str],
        command: str,
        *,
        status: str,
        result: Optional[str] = None,
        error: Optional[str] = None,
    ) -> None:
        """Publish Redis acknowledgment using Pydantic model for type safety."""
        if self._redis_proxy is None:
            return

        if status == "success":
            ack_payload = RedisAckPayload.success(message_id=message_id, command=command, result=result or "")
        else:
            ack_payload = RedisAckPayload.failure(message_id=message_id, command=command, error=error or "Unknown error")

        try:
            serialized = ack_payload.model_dump_json()
        except Exception as exc:
            logger.error(f"{LogIcons.ERROR} Failed to serialize QGC ack payload: {exc}")
            return

        try:
            self._redis_proxy.publish(channel=RedisChannels.REDIS_ACK_CHANNEL.value, message=serialized)
            if message_id:
                self._redis_proxy.publish(
                    channel=f"{RedisChannels.REDIS_ACK_CHANNEL.value}/{message_id}",
                    message=serialized,
                )
        except Exception as exc:
            logger.error(f"{LogIcons.ERROR} Failed to publish QGC ack: {exc}")

    def publish_status_update_redis(self, status: Dict[str, Any]) -> None:
        """Publish mission status updates using Pydantic models for type safety."""
        if self._redis_proxy is None or self.mission_queue.get_current_mission_id() is None:
            return

        mission_id = self.mission_queue.get_current_mission_id()
        
        plan = getattr(self.mission_queue.get_current_mission(), 'plan', None)
        plan_name = getattr(plan, 'name', None) if plan else None
        if plan_name and plan_name != mission_id:
            logger.warning(f"{LogIcons.WARNING} Mission ID mismatch: graph_id='{mission_id}' vs plan.name='{plan_name}'")
        
        message_id = f"mission-progress-{uuid.uuid4()}"
        timestamp = time.time()

        # Publish mission status update using Pydantic model
        try:
            progress_payload = RedisProgressPayload(
                message_id=message_id,
                mission_id=mission_id,
                timestamp=timestamp,
                status=status
            )
            serialized_progress = progress_payload.model_dump_json()
        except Exception as exc:
            logger.error(f"{LogIcons.ERROR} Failed to serialize mission progress payload: {exc}")
            return

        channels = [
            RedisChannels.REDIS_PROGRESS_CHANNEL.value,
            f"{RedisChannels.REDIS_PROGRESS_CHANNEL.value}/{mission_id}",
        ]

        for channel in channels:
            try:
                self._redis_proxy.publish(channel=channel, message=serialized_progress)
            except Exception as exc:
                logger.warning(f"{LogIcons.WARNING} Failed to publish mission progress on {channel}: {exc}")

        # Publish leg status updates using Pydantic model
        if status.get("next_step_id") or status.get("step_id"):
            try:
                leg_payload = RedisMissionLegPayload(
                    message_id=message_id,
                    mission_id=mission_id,
                    timestamp=timestamp,
                    current_step_id=status.get("next_step_id") or "",
                    previous_step_id=status.get("step_id"),
                    state=status.get("state"),
                    step_completed=status.get("step_completed")
                )
                serialized_leg = leg_payload.model_dump_json()
            except Exception as exc:
                logger.error(f"{LogIcons.ERROR} Failed to serialize mission leg payload: {exc}")
                return

            leg_channels = [
                RedisChannels.REDIS_MISSION_LEG_CHANNEL.value,
                f"{RedisChannels.REDIS_MISSION_LEG_CHANNEL.value}/{mission_id}",
            ]

            for channel in leg_channels:
                try:
                    self._redis_proxy.publish(channel=channel, message=serialized_leg)
                except Exception as exc:
                    logger.warning(f"{LogIcons.WARNING} Failed to publish mission leg update on {channel}: {exc}")

    
    # ══════════════════════════════════════════════════════════════════
    # §10. RTL MISSION BUILDER
    # ══════════════════════════════════════════════════════════════════
    
    def _create_rtl_mission(self) -> Optional[Dict[str, Any]]:
        """Create an RTL (Return to Launch) mission using FC home position.
        
        Returns:
            Mission plan dictionary ready to be loaded, or None if home position unavailable.
        """
        try:
            # Get home position from FC status
            home_position = self._fc_status_provider.get_home_position()
            
            if not home_position or not home_position.is_set:
                logger.error(f"{LogIcons.ERROR} Cannot create RTL mission: Home position not available from FC")
                return None
            
            if not home_position.local_ned:
                logger.error(f"{LogIcons.ERROR} Cannot create RTL mission: Home local NED position not available")
                return None
            
            # Import mission plan classes
            from leafsdk.core.mission.mission_plan import MissionPlan, MissionConfig, AutoStartBehavior, MissionLoadBehavior
            from leafsdk.core.mission.mission_plan_step import GotoLocalPosition, Land
            
            # Create mission plan (without UUID suffix for RTL)
            mission_plan = MissionPlan(name="RTL", append_uuid=False)
            
            # Configure mission to replace any running mission and wait for explicit start
            mission_plan.config.mission_load_behavior = MissionLoadBehavior.REPLACE_IF_MISSION_IN_PROGRESS
            mission_plan.config.auto_start_behavior = AutoStartBehavior.WAIT_FOR_COMMAND
            
            # Get current position (NED format: north, east, down)
            current_local = self._fc_status_provider.get_local_position()
            
            # Get home position in local NED coordinates
            home_ned = home_position.local_ned
            
            # Mission system uses ENU (East-North-Up), need to convert from NED
            # NED: (north, east, down) -> ENU: (east, north, up)
            # home_waypoint: (east, north, up)
            current_up = -current_local[2]  # NED down -> ENU up (invert sign)
            home_waypoint = (home_ned.east, home_ned.north, current_up)
            
            logger.info(
                f"{LogIcons.RUN} Creating RTL mission to home position: "
                f"Home NED=({home_ned.north:.2f}, {home_ned.east:.2f}, {home_ned.down:.2f}), "
                f"Home ENU=({home_ned.east:.2f}, {home_ned.north:.2f}, {-home_ned.down:.2f}), "
                f"Target ENU=({home_ned.east:.2f}, {home_ned.north:.2f}, {current_up:.2f}) "
                f"[Maintaining current altitude]"
            )
            
            # Add steps to mission
            # Step 1: Navigate to home position at safe RTL altitude
            mission_plan.add(
                to_name="goto_home",
                to_step=GotoLocalPosition(
                    waypoints=home_waypoint,
                    yaws_deg=0.0,  # Face north
                    speed=0.5,  # 0.5 m/s return speed (slow and safe)
                    yaw_speed="sync",
                    is_pausable=True
                )
            )
            
            # Step 2: Land at home position
            mission_plan.add(
                to_name="land",
                to_step=Land(),
                from_name="goto_home"
            )
            
            # Validate and return as dict
            mission_plan.validate()
            return mission_plan.as_dict()
            
        except Exception as e:
            logger.error(f"{LogIcons.ERROR} Failed to create RTL mission: {e}")
            logger.error(traceback.format_exc())
            return None
    
    def _create_goto_mission(self, goto_request: GotoRequest) -> Optional[Dict[str, Any]]:
        """Create a goto mission from position request.
        
        Args:
            goto_request: GotoRequest with position type, coordinates, and optional altitude
            
        Returns:
            Mission plan dictionary ready to be loaded, or None on error.
        """
        try:
            # Check if drone is flying
            drone_state = self._fc_status_provider.get_drone_state()
            if drone_state not in [DroneState.MOVING, DroneState.HOVERING, DroneState.IDLE]:
                logger.error(
                    f"{LogIcons.ERROR} Cannot create goto mission: Drone must be flying. "
                    f"Current state: {drone_state.value}"
                )
                return None
            
            # Import mission plan classes
            from leafsdk.core.mission.mission_plan import MissionPlan, AutoStartBehavior
            from leafsdk.core.mission.mission_plan_step import GotoGPSWaypoint, GotoLocalPosition, GotoRelative
            
            # Create mission plan
            mission_plan = MissionPlan(name="Goto", append_uuid=False)
            mission_plan.config.auto_start_behavior = AutoStartBehavior.AUTOSTART_ON_LOAD_IMMEDIATELY
            
            # Handle altitude - use current if not provided
            z_coord = goto_request.z
            if z_coord is None:
                current_local = self._fc_status_provider.get_local_position()
                z_coord = current_local[2]  # NED down coordinate
                logger.info(f"{LogIcons.RUN} Using current altitude: {-z_coord:.2f}m AGL (NED down: {z_coord:.2f})")
            
            # Create waypoint tuple
            waypoint = (goto_request.x, goto_request.y, z_coord)
            
            # Select appropriate step type based on position_type
            if goto_request.position_type == "gps":
                logger.info(
                    f"{LogIcons.RUN} Creating goto mission to GPS waypoint: "
                    f"lat={goto_request.x:.7f}, lon={goto_request.y:.7f}, alt={z_coord:.2f}m"
                )
                goto_step = GotoGPSWaypoint(
                    waypoints=waypoint,
                    yaws_deg=goto_request.yaw,
                    speed=goto_request.speed,
                    yaw_speed=goto_request.yaw_speed,
                    is_pausable=True
                )
            elif goto_request.position_type == "local":
                logger.info(
                    f"{LogIcons.RUN} Creating goto mission to local position: "
                    f"NED=({goto_request.x:.2f}, {goto_request.y:.2f}, {z_coord:.2f})"
                )
                goto_step = GotoLocalPosition(
                    waypoints=waypoint,
                    yaws_deg=goto_request.yaw,
                    speed=goto_request.speed,
                    yaw_speed=goto_request.yaw_speed,
                    is_pausable=True
                )
            elif goto_request.position_type == "relative":
                logger.info(
                    f"{LogIcons.RUN} Creating goto mission to relative position: "
                    f"offset=({goto_request.x:.2f}, {goto_request.y:.2f}, {z_coord:.2f})"
                )
                goto_step = GotoRelative(
                    waypoints=waypoint,
                    yaws_deg=goto_request.yaw,
                    speed=goto_request.speed,
                    yaw_speed=goto_request.yaw_speed,
                    is_pausable=True
                )
            else:
                logger.error(f"{LogIcons.ERROR} Invalid position_type: {goto_request.position_type}")
                return None
            
            # Add goto step to mission
            mission_plan.add(
                to_name="goto_position",
                to_step=goto_step
            )
            
            # Validate and return as dict
            mission_plan.validate()
            return mission_plan.as_dict()
            
        except Exception as e:
            logger.error(f"{LogIcons.ERROR} Failed to create goto mission: {e}")
            logger.error(traceback.format_exc())
            return None
    
    # ══════════════════════════════════════════════════════════════════
    # §11. MQTT COMMAND HANDLERS
    # ══════════════════════════════════════════════════════════════════

    async def _mqtt_subscribe_to_mission_plan(self):
        if self._mqtt_proxy is None:
            logger.warning(f"{LogIcons.WARNING} MQTT proxy not available. MQTT functionalities will be disabled.")
            return
        self.mqtt_subscription_id = self._mqtt_proxy.register_handler(self._mqtt_command_handler_master)
        logger.info(f"{LogIcons.SUCCESS} registered MQTT command handler with subscription ID: {self.mqtt_subscription_id}")

    async def _mqtt_command_handler_master(self, topic: str, payload: Dict[str, Any]):
        """Master MQTT command handler using Pydantic models for type safety."""
        logger.info(f"{LogIcons.RUN} [MQTT DEBUG] Received message on topic: {topic}")
        logger.info(f"{LogIcons.RUN} [MQTT DEBUG] Payload keys: {list(payload.keys())}")
        logger.info(f"{LogIcons.RUN} [MQTT DEBUG] Full payload: {payload}")
        
        try:
            mqtt_msg = MQTTCommandMessage.model_validate(payload)
            
            if mqtt_msg.command == "petal-leafsdk/mission_plan":
                logger.info(f"{LogIcons.RUN} [MQTT DEBUG] Command: {mqtt_msg.command}, MessageID: {mqtt_msg.messageId}")
                logger.info(f"{LogIcons.RUN} [MQTT DEBUG] Payload keys: {list(mqtt_msg.payload.keys())}")
                
                mission_data = mqtt_msg.payload.get("mission_plan_json")
                if mission_data is None:
                    logger.error(f"{LogIcons.ERROR} Missing mission_plan_json in MQTT payload")
                    error_response = MQTTResponseMessage(
                        messageId=mqtt_msg.messageId,
                        status="error",
                        error="Missing mission_plan_json in payload"
                    )
                    await self._mqtt_proxy.publish_message(error_response.model_dump())
                    return
                
                asyncio.create_task(
                    self._mqtt_command_handler_mission_plan(mqtt_msg.messageId, mission_data)
                )
            
            elif mqtt_msg.command == "petal-leafsdk/rtl":
                logger.info(f"{LogIcons.RUN} [MQTT] RTL command received, MessageID: {mqtt_msg.messageId}")
                asyncio.create_task(
                    self._mqtt_command_handler_rtl(mqtt_msg.messageId)
                )
            
            elif mqtt_msg.command == "petal-leafsdk/goto":
                logger.info(f"{LogIcons.RUN} [MQTT] Goto command received, MessageID: {mqtt_msg.messageId}")
                goto_data = mqtt_msg.payload
                asyncio.create_task(
                    self._mqtt_command_handler_goto(mqtt_msg.messageId, goto_data)
                )
        except Exception as exc:
            logger.error(f"{LogIcons.ERROR} MQTT command handler validation error: {exc}")
            try:
                message_id = payload.get('messageId', 'unknown')
                error_response = MQTTResponseMessage(
                    messageId=message_id,
                    status="error",
                    error=f"Invalid MQTT message format: {exc}"
                )
                await self._mqtt_proxy.publish_message(error_response.model_dump())
            except Exception as publish_exc:
                logger.error(f"{LogIcons.ERROR} Failed to send MQTT error response: {publish_exc}")

    async def _mqtt_command_handler_mission_plan(self, msg_id: str, data: Dict[str, Any]):
        """Handle mission plan command from MQTT using Pydantic models."""
        try:
            logger.info(f"{LogIcons.SUCCESS} Received mission plan via MQTT.")
            try:
                validated_mission = MissionPlanDTO.model_validate(data)
                mission_dict = validated_mission.model_dump(by_alias=True)
                success, message, error = self._validate_and_enqueue_mission(mission_dict)
            except Exception as validation_exc:
                logger.error(f"{LogIcons.ERROR} MQTT mission validation failed: {validation_exc}")
                success, message, error = False, "Mission validation failed", str(validation_exc)
            
            response = MQTTResponseMessage(
                messageId=msg_id,
                status="success" if success else "error",
                result=message if success else None,
                error=error if not success else None
            )
            await self._mqtt_proxy.publish_message(response.model_dump())
            
            return {f"{'success' if success else 'error'}: {message} {'' if success else f', error: {error}'}"}
        except Exception as exc:
            logger.error(f"{LogIcons.ERROR} MQTT mission handler error: {exc}")
            try:
                error_response = MQTTResponseMessage(
                    messageId=msg_id,
                    status="error",
                    error=str(exc)
                )
                await self._mqtt_proxy.publish_message(error_response.model_dump())
            except Exception as publish_exc:
                logger.error(f"{LogIcons.ERROR} Failed to send MQTT error response: {publish_exc}")
            return {"error": str(exc)}
    
    async def _mqtt_command_handler_rtl(self, msg_id: str):
        """Handle RTL (Return to Launch) command from MQTT."""
        try:
            logger.info(f"{LogIcons.RUN} Creating RTL mission...")
            
            # Create RTL mission from FC home position
            rtl_mission_dict = self._create_rtl_mission()
            
            if rtl_mission_dict is None:
                error_msg = "Failed to create RTL mission: Home position not available"
                logger.error(f"{LogIcons.ERROR} {error_msg}")
                error_response = MQTTResponseMessage(
                    messageId=msg_id,
                    status="error",
                    error=error_msg
                )
                await self._mqtt_proxy.publish_message(error_response.model_dump())
                return {"error": error_msg}
            
            # Load and start the RTL mission
            logger.info(f"{LogIcons.SUCCESS} RTL mission created, loading...")
            success, message, error = self._validate_and_enqueue_mission(rtl_mission_dict)
            
            response = MQTTResponseMessage(
                messageId=msg_id,
                status="success" if success else "error",
                result=message if success else None,
                error=error if not success else None
            )
            await self._mqtt_proxy.publish_message(response.model_dump())
            
            if success:
                logger.info(f"{LogIcons.SUCCESS} RTL mission loaded and started: {message}")
            else:
                logger.error(f"{LogIcons.ERROR} RTL mission failed: {error}")
            
            return {f"{'success' if success else 'error'}: {message} {'' if success else f', error: {error}'}"}
            
        except Exception as exc:
            logger.error(f"{LogIcons.ERROR} RTL handler error: {exc}")
            logger.error(traceback.format_exc())
            try:
                error_response = MQTTResponseMessage(
                    messageId=msg_id,
                    status="error",
                    error=str(exc)
                )
                await self._mqtt_proxy.publish_message(error_response.model_dump())
            except Exception as publish_exc:
                logger.error(f"{LogIcons.ERROR} Failed to send MQTT error response: {publish_exc}")
            return {"error": str(exc)}
    
    async def _mqtt_command_handler_goto(self, msg_id: str, goto_data: Dict[str, Any]):
        """Handle goto command from MQTT."""
        try:
            logger.info(f"{LogIcons.RUN} Processing goto command...")
            
            # Validate goto request data
            try:
                goto_request = GotoRequest.model_validate(goto_data)
            except Exception as validation_exc:
                error_msg = f"Invalid goto request: {validation_exc}"
                logger.error(f"{LogIcons.ERROR} {error_msg}")
                error_response = MQTTResponseMessage(
                    messageId=msg_id,
                    status="error",
                    error=error_msg
                )
                await self._mqtt_proxy.publish_message(error_response.model_dump())
                return {"error": error_msg}
            
            # Create goto mission
            goto_mission_dict = self._create_goto_mission(goto_request)
            
            if goto_mission_dict is None:
                error_msg = "Failed to create goto mission: Check drone state and position validity"
                logger.error(f"{LogIcons.ERROR} {error_msg}")
                error_response = MQTTResponseMessage(
                    messageId=msg_id,
                    status="error",
                    error=error_msg
                )
                await self._mqtt_proxy.publish_message(error_response.model_dump())
                return {"error": error_msg}
            
            # Load and start the goto mission
            logger.info(f"{LogIcons.SUCCESS} Goto mission created, loading...")
            success, message, error = self._validate_and_enqueue_mission(goto_mission_dict)
            
            response = MQTTResponseMessage(
                messageId=msg_id,
                status="success" if success else "error",
                result=message if success else None,
                error=error if not success else None
            )
            await self._mqtt_proxy.publish_message(response.model_dump())
            
            if success:
                logger.info(f"{LogIcons.SUCCESS} Goto mission loaded and started: {message}")
            else:
                logger.error(f"{LogIcons.ERROR} Goto mission failed: {error}")
            
            return {f"{'success' if success else 'error'}: {message} {'' if success else f', error: {error}'}"}
            
        except Exception as exc:
            logger.error(f"{LogIcons.ERROR} Goto handler error: {exc}")
            logger.error(traceback.format_exc())
            try:
                error_response = MQTTResponseMessage(
                    messageId=msg_id,
                    status="error",
                    error=str(exc)
                )
                await self._mqtt_proxy.publish_message(error_response.model_dump())
            except Exception as publish_exc:
                logger.error(f"{LogIcons.ERROR} Failed to send MQTT error response: {publish_exc}")
            return {"error": str(exc)}