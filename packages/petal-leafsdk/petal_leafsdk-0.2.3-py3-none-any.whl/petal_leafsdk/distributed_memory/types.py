"""
Shared types and data structures for distributed state synchronization.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Any
import asyncio


class SyncResult(Enum):
    """Result of a state synchronization operation."""
    SUCCESS = "success"
    TIMEOUT = "timeout"
    REJECTED = "rejected"
    INVALID_TRANSITION = "invalid_transition"
    ERROR = "error"


@dataclass
class StateChangeRequest:
    """
    Tracks a pending state change request awaiting validation.
    
    Used by MissionStateSynchronizer to track mission state changes
    that need FC acknowledgment.
    """
    request_id: str
    mission_id: str
    from_state: str
    to_state: str
    command_type: str  # "run", "pause", "resume", "abort"
    timestamp: float
    
    # ACK tracking
    ack_received: bool = False
    ack_success: bool = False
    ack_event: asyncio.Event = field(default_factory=asyncio.Event)
    
    # Result
    result: Optional[SyncResult] = None
    error_message: Optional[str] = None

    def complete(self, success: bool, error: Optional[str] = None):
        """Mark request as complete and unblock waiters."""
        self.ack_received = True
        self.ack_success = success
        self.result = SyncResult.SUCCESS if success else SyncResult.REJECTED
        self.error_message = error
        self.ack_event.set()


@dataclass
class FCStateSnapshot:
    """
    Snapshot of FC state at a point in time.
    
    Used for state history tracking and debugging.
    """
    timestamp: float
    drone_state: str
    leaf_status: Optional[int]
    leaf_mission_status: Optional[int]
    leaf_mode: Optional[int]
    fc_armed: bool
    fc_connected: bool
