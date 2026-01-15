import time
from typing import List, Optional

from leafsdk.utils.logstyle import LogIcons
from petal_leafsdk import logger

# --- Shared Data Store ---
class LocalDataStore:
    """
    Holds local copies of system data for the MissionManager. 
    Updates happen instantly; no need to query external systems.
    """
    def __init__(self):
        # System
        self.last_update_source: str = ""
        self.last_update_timestamp: float = 0.0

    def update(self, key, value):
        setattr(self, key, value)
        self.last_update_timestamp = time.time()
        logger.debug(f"{LogIcons.INFO} [DataStore Updated] {key} = {value}")

class MissionManagerLocalDataStore(LocalDataStore):
    def __init__(self):
        super().__init__()
        # Mission state
        self.mission_id: Optional[str] = None
        self.mission_state: Optional[str] = None  # MissionStateAll.name
        self.mission_name: Optional[str] = None
        
        # Queue state
        self.queue_size: int = 0
        self.queue_front_id: Optional[str] = None
        
        # FC state
        self.fc_connected: bool = False
        self.drone_state: Optional[str] = None  # DroneState.name
        
        # System
        self.last_update_source: str = ""
        self.last_update_timestamp: float = 0.0

# --- The Central Manager ---
class CentralizedStatusManager:
    """
    Central hub for status data. Modules register to receive notifications
    when other modules update data.
    """
    def __init__(self):
        self.data_store = MissionManagerLocalDataStore()
        self._registered_modules: List['ExternalCentralizedStatus'] = []

    def start(self):
        """Initialize the manager."""
        logger.info(f"{LogIcons.SUCCESS} CentralizedStatusManager started")

    def register(self, module: 'ExternalCentralizedStatus'):
        """Register a status module to receive update notifications."""
        if module not in self._registered_modules:
            self._registered_modules.append(module)
            logger.info(f"{LogIcons.SUCCESS} [Manager] Registered: {module.name}")

    def unregister(self, module: 'ExternalCentralizedStatus'):
        """Unregister a status module."""
        if module in self._registered_modules:
            self._registered_modules.remove(module)
            logger.info(f"{LogIcons.SUCCESS} [Manager] Unregistered: {module.name}")

    def update(self, source: 'ExternalCentralizedStatus', data: dict):
        """
        Called when any module wants to update data.
        Updates the data store, then notifies ALL other registered modules.
        """
        logger.debug(f"{LogIcons.RUN} [Manager] Update from {source.name}: {data}")
        self.data_store.last_update_source = source.name
        
        # 1. Update local data store
        for key, value in data.items():
            self.data_store.update(key, value)
        
        # 2. Notify ALL other registered modules
        for module in self._registered_modules:
            if module != source:  # Don't notify the source itself
                module.on_data_changed(source.name, data)

    def get(self, key):
        return self.data_store.get(key)

# --- External Centralized Status Modules ---
class ExternalCentralizedStatus:
    """
    Base class for status modules.
    Modules register with the manager and receive notifications when data changes.
    """
    def __init__(self, name: str, manager: CentralizedStatusManager):
        self.name = name
        self.manager = manager

    def register(self):
        """Register this module with the manager."""
        self.manager.register(self)

    def update(self, data: dict):
        """
        Push data update through the manager.
        This will trigger on_data_changed on all OTHER registered modules.
        """
        self.manager.update(self, data)

    def on_data_changed(self, source_name: str, data: dict):
        """
        Called by the manager when another module updates data.
        Override this in subclasses to implement specific logic.
        """
        logger.debug(f"{LogIcons.INFO} [{self.name}] on_data_changed from {source_name}: {data}")
        self.handle_update(source_name, data)

    def handle_update(self, source_name: str, data: dict):
        """Override this to implement custom update logic."""
        pass


# --- MissionManager Specific Implementations ---
class Centralized_Status_Queue(ExternalCentralizedStatus):
    """Queue status module - reacts to mission state changes."""
    
    def handle_update(self, source_name: str, data: dict):
        if "mission_state" in data:
            state = data["mission_state"]
            if state in ["COMPLETED", "FAILED", "CANCELLED"]:
                logger.info(f"{LogIcons.INFO} [{self.name}] Mission ended with state '{state}' - queue may need update")


class Centralized_Status_Mission(ExternalCentralizedStatus):
    """Mission status module - reacts to FC and queue changes."""
    
    def handle_update(self, source_name: str, data: dict):
        if "drone_state" in data:
            if data["drone_state"] == "LANDING":
                logger.info(f"{LogIcons.PAUSE} [{self.name}] FC is landing - mission may need pause")


class Centralized_Status_FC(ExternalCentralizedStatus):
    """Flight Controller status module - reacts to mission/queue changes."""
    
    def handle_update(self, source_name: str, data: dict):
        if "mission_state" in data:
            logger.debug(f"{LogIcons.INFO} [{self.name}] Mission state changed to: {data['mission_state']}")


# --- Execution ---
if __name__ == "__main__":
    # Configure basic logging for demo
    import logging
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    
    mgr = CentralizedStatusManager()
    mgr.start()

    # Create centralized status modules
    queue = Centralized_Status_Queue("CENTRALIZED_STATUS_QUEUE", mgr)
    mission = Centralized_Status_Mission("CENTRALIZED_STATUS_MISSION", mgr)
    fc = Centralized_Status_FC("CENTRALIZED_STATUS_FC", mgr)

    # Register them with the manager
    queue.register()
    mission.register()
    fc.register()

    print("\n" + "="*60)
    print("DEMO: Queue updates data -> Mission and FC get notified")
    print("="*60)
    
    # When Queue updates, Mission's and FC's on_data_changed is triggered
    queue.update({"queue_size": 3, "queue_front_id": "mission-001"})

    print("\n" + "="*60)
    print("DEMO: Mission updates state -> Queue and FC get notified")
    print("="*60)
    
    # When Mission updates, Queue's and FC's on_data_changed is triggered
    mission.update({"mission_id": "mission-001", "mission_state": "RUNNING"})

    print("\n" + "="*60)
    print("DEMO: FC updates drone state -> Queue and Mission get notified")
    print("="*60)
    
    # When FC updates, Queue's and Mission's on_data_changed is triggered
    fc.update({"drone_state": "LANDING", "fc_connected": True})

    print("\n" + "="*60)
    print("DEMO: Mission completion -> triggers queue handle_update logic")
    print("="*60)
    
    mission.update({"mission_id": "mission-001", "mission_state": "COMPLETED"})