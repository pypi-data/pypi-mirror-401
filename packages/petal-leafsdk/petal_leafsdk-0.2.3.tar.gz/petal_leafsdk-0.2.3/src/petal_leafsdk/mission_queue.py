import time
from typing import Any, Dict, Optional, TYPE_CHECKING
from . import logger
from leafsdk.utils.logstyle import LogIcons
from leafsdk.core.mission.mission_plan import MissionConfig

if TYPE_CHECKING:
    from petal_leafsdk.fsm import CentralizedStatusManager


class MissionQueue:
    """
    FIFO (First-In-First-Out) queue for managing mission graphs.
    
    Queue Discipline:
    - Standard behavior: FIFO - items are processed in arrival order
    - Index 0 is ALWAYS the currently running or next-to-run mission
    - Out-of-order execution: Use promote_to_front() to move a mission to index 0
    
    Supports configurable capacity, priority inspection, and mission lifecycle tracking.
    Each item in queue has 'id' and 'data' attributes.
    
    Scientific Queue Patterns:
    - FIFO (First-In-First-Out): Default behavior
    - Priority Promotion: Via promote_to_front() for urgent missions
    """
    
    def __init__(self, max_size: int = 10, failed_missions: Optional['MissionQueue'] = None, previous_missions: Optional['MissionQueue'] = None, status_manager: Optional['CentralizedStatusManager'] = None):
        """
        Initialize mission queue.
        
        Args:
            max_size: Maximum number of missions that can be queued (default: 10)
            failed_missions: Dead-letter queue for failed missions (optional)
            previous_missions: History queue for completed missions (optional)
            status_manager: CentralizedStatusManager for state notifications (optional)
        """
        self.items = []
        self.max_size = max_size
        self._enqueue_count = 0
        self._dequeue_count = 0
        self._peak_size = 0
        
        self.failed_missions = failed_missions
        self.previous_missions = previous_missions
        
        # Centralized status management
        self._centralized_status_manager = status_manager
        self._centralized_status_queue = None
        if status_manager:
            from petal_leafsdk.fsm import Centralized_Status_Queue
            self._centralized_status_queue = Centralized_Status_Queue("CENTRALIZED_STATUS_QUEUE", status_manager)
            self._centralized_status_queue.register()
            logger.info(f"{LogIcons.SUCCESS} MissionQueue: Centralized_Status_Queue registered")

    def is_empty(self) -> bool:
        """Check if queue has no items."""
        return len(self.items) == 0

    def is_full(self) -> bool:
        """Check if queue has reached maximum capacity."""
        return len(self.items) >= self.max_size

    def enqueue(self, id: str, data: Any, allow_duplicate_names, mission_name: Optional[str] = None) -> tuple[bool, Optional[str]]:
        """
        Add mission to the end of the queue.
        
        Args:
            id: Mission identifier (unique mission ID)
            data: Mission instance (Mission)
            allow_duplicate_names: AllowDuplicateNames enum (ALLOW, OVERRIDE, FAIL)
            mission_name: Mission name for duplicate checking
            
        Returns:
            Tuple of (success: bool, error_message: Optional[str])
        """
        if self.is_full():
            error_msg = f"Queue is full ({self.max_size} items). Cannot enqueue mission '{mission_name or id}'."
            logger.warning(f"{LogIcons.WARNING} {error_msg}")
            return False, error_msg
        
        if mission_name:
            existing_item = self.find_by_name(mission_name)
            if existing_item is not None:
                from leafsdk.core.mission.mission_plan import AllowDuplicateNames
                
                if allow_duplicate_names == AllowDuplicateNames.FAIL:
                    error_msg = f"Mission with name '{mission_name}' already exists in queue (ID: '{existing_item['id']}'). FAIL policy - rejecting."
                    logger.warning(f"{LogIcons.WARNING} {error_msg}")
                    return False, error_msg
                elif allow_duplicate_names == AllowDuplicateNames.OVERRIDE:
                    logger.info(f"{LogIcons.RUN} Replacing mission with name '{mission_name}' (ID: '{existing_item['id']}') due to OVERRIDE policy.")
                    self.remove_by_id(existing_item['id'])
        
        self.items.append({"id": id, "data": data})
        self._enqueue_count += 1
        
        if len(self.items) > self._peak_size:
            self._peak_size = len(self.items)
        
        # Notify centralized status manager of queue update
        if self._centralized_status_queue:
            self._centralized_status_queue.update({
                "queue_size": self.size(),
                "queue_front_id": self.get_current_mission_id(),
            })
        
        logger.info(f"{LogIcons.SUCCESS} Mission '{id}' enqueued (position: {len(self.items)})")
        return True, None

    def dequeue(self) -> Optional[Dict[str, Any]]:
        """
        Remove and return the first mission from queue.
        
        Returns:
            Dict with 'id' and 'data' keys, or None if queue is empty
        """
        if self.is_empty():
            return None
        
        self._dequeue_count += 1
        item = self.items.pop(0)
        logger.info(f"{LogIcons.SUCCESS} Mission '{item['id']}' dequeued")
        if self._centralized_status_queue:
            self._centralized_status_queue.update({
                "queue_size": self.size(),
                "queue_front_id": self.get_current_mission_id(),
            })
        return item

    def peek(self) -> Optional[Dict[str, Any]]:
        """
        View the next mission without removing it.
        
        Returns:
            Dict with 'id' and 'data' keys, or None if queue is empty
        """
        if self.is_empty():
            return None
        return self.items[0]
    
    def get_current_mission(self):
        """
        Get the mission instance for the current mission (position 0).
        
        Returns:
            Mission instance or None if queue is empty
        """
        item = self.peek()
        return item["data"] if item else None
    
    def get_current_mission_id(self) -> Optional[str]:
        """
        Get the mission ID for the current mission (position 0).
        
        Returns:
            Mission ID string or None if queue is empty
        """
        item = self.peek()
        return item["id"] if item else None

    def peek_at(self, index: int) -> Optional[Dict[str, Any]]:
        """
        View mission at specific position without removing it.
        
        Args:
            index: Position in queue (0 = front)
            
        Returns:
            Dict with 'id' and 'data' keys, or None if index out of range
        """
        if index < 0 or index >= len(self.items):
            return None
        return self.items[index]

    def find_by_id(self, mission_id: str) -> Optional[Dict[str, Any]]:
        """
        Find mission by ID without removing it.
        
        Args:
            mission_id: Mission identifier to search for
            
        Returns:
            Dict with 'id' and 'data' keys, or None if not found
        """
        for item in self.items:
            if item["id"] == mission_id:
                return item
        return None

    def find_by_name(self, mission_name: str) -> Optional[Dict[str, Any]]:
        """
        Find mission by name without removing it.
        
        Mission name is extracted from the mission's mission_name attribute.
        This is used to check for duplicate mission names in the queue.
        
        Args:
            mission_name: Mission name to search for (original name from data["id"])
            
        Returns:
            Dict with 'id' and 'data' keys, or None if not found
        """
        for item in self.items:
            mission = item["data"]
            if hasattr(mission, 'mission_name') and mission.mission_name == mission_name:
                return item
        return None

    def remove_by_id(self, mission_id: str) -> bool:
        """
        Remove mission by ID from queue (regardless of position).
        
        Args:
            mission_id: Mission identifier to remove
            
        Returns:
            True if mission was found and removed, False otherwise
        """
        for i, item in enumerate(self.items):
            if item["id"] == mission_id:
                self.items.pop(i)
                logger.info(f"{LogIcons.SUCCESS} Mission '{mission_id}' removed from queue")
                self._dequeue_count += 1
                return True
        logger.warning(f"{LogIcons.WARNING} Mission '{mission_id}' not found in queue")
        return False

    def promote_to_front(self, mission_id: str) -> bool:
        """
        Move a mission to index 0 (front of queue) for immediate execution.
        This implements out-of-order execution by promoting a queued mission.
        
        Queue Discipline: This breaks FIFO ordering but ensures the running
        mission is always at index 0.
        
        Args:
            mission_id: Mission identifier to promote
            
        Returns:
            True if mission was found and promoted, False otherwise
        """
        for i, item in enumerate(self.items):
            if item["id"] == mission_id:
                if i == 0:
                    logger.info(f"{LogIcons.SUCCESS} Mission '{mission_id}' already at front")
                    return True
                promoted_item = self.items.pop(i)
                self.items.insert(0, promoted_item)
                logger.info(f"{LogIcons.SUCCESS} Mission '{mission_id}' promoted from position {i} to front (index 0)")
                if self._centralized_status_queue:
                    self._centralized_status_queue.update({
                        "queue_size": self.size(),
                        "queue_front_id": self.get_current_mission_id(),
                    })
                return True
        logger.warning(f"{LogIcons.WARNING} Mission '{mission_id}' not found in queue for promotion")
        return False

    def get_position(self, mission_id: str) -> int:
        """
        Get position of mission in queue.
        
        Args:
            mission_id: Mission identifier
            
        Returns:
            Position index (0-based), or -1 if not found
        """
        for i, item in enumerate(self.items):
            if item["id"] == mission_id:
                return i
        return -1

    def size(self) -> int:
        """Get current number of missions in queue."""
        return len(self.items)

    def clear(self) -> int:
        """
        Remove all missions from queue.
        
        Returns:
            Number of missions that were cleared
        """
        count = len(self.items)
        self.items.clear()
        logger.info(f"{LogIcons.SUCCESS} Queue cleared ({count} missions removed)")
        if self._centralized_status_queue:
            self._centralized_status_queue.update({
                "queue_size": self.size(),
                "queue_front_id": self.get_current_mission_id(),
            })
        return count

    def get_all(self) -> list:
        """
        Get copy of all queued missions (does not modify queue).
        
        Returns:
            List of all mission items (dicts with 'id' and 'data') in queue order
        """
        return self.items.copy()

    def get_all_ids(self) -> list:
        """
        Get list of all mission IDs in queue order.
        
        Returns:
            List of mission IDs
        """
        return [item["id"] for item in self.items]

    def contains_id(self, mission_id: str) -> bool:
        """
        Check if mission with specific ID is in queue.
        
        Args:
            mission_id: Mission identifier to search for
            
        Returns:
            True if mission exists in queue
        """
        return any(item["id"] == mission_id for item in self.items)

    def get_stats(self) -> Dict[str, Any]:
        """
        Get queue statistics for monitoring.
        
        Returns:
            Dictionary with queue metrics
        """
        return {
            "current_size": len(self.items),
            "max_size": self.max_size,
            "peak_size": self._peak_size,
            "total_enqueued": self._enqueue_count,
            "total_dequeued": self._dequeue_count,
            "is_empty": self.is_empty(),
            "is_full": self.is_full(),
            "queued_mission_ids": self.get_all_ids()
        }

    def __len__(self) -> int:
        """Support len() function."""
        return len(self.items)

    def __contains__(self, mission_id: str) -> bool:
        """Support 'in' operator for mission ID lookup."""
        return self.contains_id(mission_id)

    def __repr__(self) -> str:
        """String representation for debugging."""
        ids = ", ".join(item["id"] for item in self.items[:3])
        if len(self.items) > 3:
            ids += f"... (+{len(self.items) - 3} more)"
        return f"MissionQueue(size={len(self.items)}/{self.max_size}, missions=[{ids}])"

    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"Mission Queue: {len(self.items)} of {self.max_size} slots used"
    
    def handle_mission_success(self) -> Dict[str, Any]:
        """
        Handle successful mission completion based on MissionSuccessfulCompletionBehavior.
        Operates on the mission at the front of the queue (index 0).
        Encapsulates all queue manipulation logic and returns action instructions.
        
        Returns:
            Dict with keys:
                - 'action': 'idle' | 'load_next' | 'restart_mission'
                - 'next_mission_id': ID of next mission to load (if action == 'load_next' or 'restart_mission')
                - 'message': Human-readable status message
        """
        # Get mission data at front of queue
        mission_item = self.peek()
        if not mission_item:
            logger.warning(f"{LogIcons.WARNING} No mission in queue to mark as successful")
            return {'action': 'idle', 'message': 'No mission in queue'}
        
        mission_id = mission_item['id']
        
        # Only DEQUEUE_AND_LOAD_NEXT is supported
        removed = self.dequeue()
        if removed and self.previous_missions:
            removed["completion_timestamp"] = time.time()
            removed["status"] = "completed_successfully"
            self.previous_missions.enqueue(
                id=removed["id"],
                data=removed,
                allow_duplicate_names=None,
                mission_name=None
            )
            logger.info(f"{LogIcons.SUCCESS} Completed mission '{mission_id}' dequeued")
        
        if not self.is_empty():
            next_mission = self.peek()
            logger.info(f"{LogIcons.RUN} Next mission ready: '{next_mission['id']}'")
            return {
                'action': 'load_next',
                'next_mission_id': next_mission['id'],
                'message': f"Loading next mission: '{next_mission['id']}'"
            }
        else:
            logger.info(f"{LogIcons.SUCCESS} Mission queue is now empty")
            return {'action': 'idle', 'message': 'Mission queue is empty'}
    
    def handle_mission_failure(self) -> Dict[str, Any]:
        """
        Handle failed mission - dequeues and loads next mission in queue.
        Operates on the mission at the front of the queue (index 0).
        Encapsulates all queue manipulation logic and returns action instructions.
        
        Returns:
            Dict with keys:
                - 'action': 'idle' | 'load_next'
                - 'next_mission_id': ID of next mission to load (if action == 'load_next')
                - 'message': Human-readable status message
        """
        mission_item = self.peek()
        if not mission_item:
            logger.warning(f"{LogIcons.WARNING} No mission in queue to mark as failed")
            return {'action': 'idle', 'message': 'No mission in queue'}
        
        mission_id = mission_item['id']
        
        # Only DEQUEUE_AND_LOAD_NEXT is supported
        removed = self.dequeue()
        if removed and self.failed_missions:
            removed["failure_timestamp"] = time.time()
            removed["failure_reason"] = "Mission execution failed"
            self.failed_missions.enqueue(
                id=removed["id"],
                data=removed,
                allow_duplicate_names=None,
                mission_name=None
            )
            logger.info(f"{LogIcons.SUCCESS} Failed mission '{mission_id}' dequeued")
        
        if not self.is_empty():
            next_mission = self.peek()
            logger.info(f"{LogIcons.RUN} Next mission ready after failure: '{next_mission['id']}'")
            return {
                'action': 'load_next',
                'next_mission_id': next_mission['id'],
                'message': f"Loading next mission after failure: '{next_mission['id']}'"
            }
        else:
            return {'action': 'idle', 'message': 'Mission queue is empty after failure'}
