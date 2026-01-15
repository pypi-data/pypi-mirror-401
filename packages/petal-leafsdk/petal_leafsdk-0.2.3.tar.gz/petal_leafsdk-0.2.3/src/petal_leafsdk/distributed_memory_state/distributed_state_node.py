"""
Distributed Memory State

Generic state synchronization with proposed state tracking.
Triggers an action when remote state differs from both current AND proposed state.
"""

from typing import TypeVar, Generic, Optional, Callable
from enum import Enum

# Generic type for any Enum-based state
StateT = TypeVar('StateT', bound=Enum)


class DistributedMemoryState(Generic[StateT]):
    """
    Generic distributed memory state with proposed state tracking.
    
    Tracks three states:
    - current_state: What we believe the state is
    - proposed_state: What we want the state to become (pending confirmation)
    - remote_state: What the remote system reports
    
    Triggers on_mismatch_action when remote state differs from 
    both current AND proposed state.
    
    Usage:
        from petal_leafsdk.mission import MissionStateAll
        
        state = DistributedMemoryState[MissionStateAll](
            initial_state=MissionStateAll.IDLE,
            on_propose_action=send_to_fc,
            on_mismatch_action=handle_fc_mismatch
        )
    """
    
    def __init__(
        self,
        initial_state: StateT,
        on_propose_action: Optional[Callable[[StateT], None]] = None,
        on_mismatch_action: Optional[Callable[[StateT], None]] = None
    ):
        """
        Initialize distributed memory state.
        
        Args:
            initial_state: Initial current state
            on_propose_action: Callback(proposed_state) triggered when propose() is called.
                              Use this to send commands to the remote system.
            on_mismatch_action: Callback(remote_state) triggered when
                               remote != current AND remote != proposed
        """
        self._current_state: StateT = initial_state
        self._proposed_state: Optional[StateT] = None
        self._remote_state: Optional[StateT] = None
        self.on_propose_action = on_propose_action
        self.on_mismatch_action = on_mismatch_action
    
    @property
    def current_state(self) -> StateT:
        return self._current_state
    
    @property
    def proposed_state(self) -> Optional[StateT]:
        return self._proposed_state
    
    @property
    def remote_state(self) -> Optional[StateT]:
        return self._remote_state
    
    def propose(self, new_state: StateT):
        """Propose a state change and trigger the action callback."""
        self._proposed_state = new_state
        if self.on_propose_action:
            self.on_propose_action(new_state)
    
    def confirm(self):
        """Confirm the proposed state as the current state."""
        if self._proposed_state is not None:
            self._current_state = self._proposed_state
            self._proposed_state = None
    
    def cancel_proposal(self):
        """Cancel the pending proposal."""
        self._proposed_state = None
    
    def update_remote_state(self, remote_state: StateT):
        """Update remote state and trigger mismatch callback if needed."""
        self._remote_state = remote_state
        
        if remote_state != self._current_state:
            if self._proposed_state is None or remote_state != self._proposed_state:
                if self.on_mismatch_action:
                    self.on_mismatch_action(remote_state)
    
    def sync_to_remote(self):
        """Sync current state to match remote state."""
        if self._remote_state is not None:
            self._current_state = self._remote_state
            self._proposed_state = None
    
    def set_state(self, new_state: StateT):
        """Directly set current state (use sparingly)."""
        self._current_state = new_state
