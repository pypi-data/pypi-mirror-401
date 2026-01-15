# petal_leafsdk/data_model.py

from pydantic import BaseModel, Field, model_validator
from typing import Annotated, Any, List, Optional, Literal, Union, Tuple, Sequence, Dict
from enum import Enum
from leafsdk.core.mission.mission_plan import (
    JoystickMode, 
    MissionConfig,
    MissionLoadBehavior,
    AllowDuplicateNames,
    AutoStartBehavior,
    StartingPointBehavior,
    PauseBehavior,
    MissionSuccessfulCompletionBehavior,
    MissionUnsuccessfulCompletionBehavior
)

Tuple3D = Tuple[float, float, float]   # exact length 3

# Mission schema
class TakeoffParams(BaseModel):
    alt: float

class GotoLocalPositionParams(BaseModel):
    waypoints: Union[Tuple3D, Sequence[Tuple3D]]
    yaws_deg: Optional[Union[float, Sequence[float]]] = 0.0
    speed: Optional[Union[float, Sequence[float]]] = 0.2
    yaw_speed: Optional[Union[float, Sequence[float], Literal["sync"]]] = "sync"
    is_pausable: bool = True
    average_deceleration: float = 0.5   # m2/s

class GotoGPSWaypointParams(BaseModel):
    waypoints: Union[Tuple3D, Sequence[Tuple3D]]
    yaws_deg: Optional[Union[float, Sequence[float]]] = 0.0
    speed: Optional[Union[float, Sequence[float]]] = 0.2
    yaw_speed: Optional[Union[float, Sequence[float], Literal["sync"]]] = "sync"
    is_pausable: bool = True
    average_deceleration: float = 0.5   # m2/s

class GotoRelativeParams(BaseModel):
    waypoints: Union[Tuple3D, Sequence[Tuple3D]]
    yaws_deg: Optional[Union[float, Sequence[float]]] = 0.0
    speed: Optional[Union[float, Sequence[float]]] = 0.2
    yaw_speed: Optional[Union[float, Sequence[float], Literal["sync"]]] = "sync"
    is_pausable: bool = True
    average_deceleration: float = 0.5   # m2/s

class YawAbsoluteParams(BaseModel):
    yaws_deg: Union[float, Sequence[float]]
    yaw_speed: Optional[Union[float, Sequence[float]]] = 30.0
    is_pausable: bool = True
    average_deceleration: float = 0.5   # m2/s

class YawRelativeParams(BaseModel):
    yaws_deg: Union[float, Sequence[float]]
    yaw_speed: Optional[Union[float, Sequence[float]]] = 30.0
    is_pausable: bool = True
    average_deceleration: float = 0.5   # m2/s

class WaitParams(BaseModel):
    duration: float

class TakeoffNode(BaseModel):
    name: str
    type: Literal["Takeoff"]
    params: TakeoffParams

class GotoLocalPositionNode(BaseModel):
    name: str
    type: Literal["GotoLocalPosition"]
    params: GotoLocalPositionParams

class GotoGPSWaypointNode(BaseModel):
    name: str
    type: Literal["GotoGPSWaypoint"]
    params: GotoGPSWaypointParams

class GotoRelativeNode(BaseModel):
    name: str
    type: Literal["GotoRelative"]
    params: GotoRelativeParams

class YawAbsoluteNode(BaseModel):
    name: str
    type: Literal["YawAbsolute"]
    params: YawAbsoluteParams

class YawRelativeNode(BaseModel):
    name: str
    type: Literal["YawRelative"]
    params: YawRelativeParams

class WaitNode(BaseModel):
    name: str
    type: Literal["Wait"]
    params: WaitParams

class LandNode(BaseModel):
    name: str
    type: Literal["Land"]
    params: Optional[dict] = None

class Edge(BaseModel):
    from_: str = Field(..., alias="from")
    to: str
    condition: Optional[str] = None

    model_config = {"populate_by_name": True}

Node = Annotated[
    Union[TakeoffNode, GotoLocalPositionNode, GotoGPSWaypointNode, 
          GotoRelativeNode, YawAbsoluteNode, YawRelativeNode, WaitNode, LandNode],
    Field(discriminator='type')
]


class MissionStepProgress(BaseModel):
    completed_mission_step_id: str
    completed_mission_step_description: Optional[str] = ""
    next_mission_step_id: str
    next_mission_step_description: Optional[str] = ""

class ProgressUpdateSubscription(BaseModel):
    address: str  # e.g., http://localhost:5000/WHMS/v1/update_step_progress

class GotoRequest(BaseModel):
    """Request to create a goto mission dynamically."""
    position_type: Literal["gps", "local", "relative"] = Field(
        ..., 
        description="Type of position coordinates: 'gps' (lat/lon/alt), 'local' (NED), 'relative' (from current)"
    )
    x: float = Field(..., description="Latitude (gps), North (local), or relative North (relative) in meters or degrees")
    y: float = Field(..., description="Longitude (gps), East (local), or relative East (relative) in meters or degrees")
    z: Optional[float] = Field(
        None, 
        description="Altitude/Down coordinate. If None, uses current altitude. For GPS: MSL altitude (m), for local/relative: NED down (m)"
    )
    yaw: Optional[float] = Field(0.0, description="Target yaw in degrees (0-360, 0=North)")
    speed: Optional[float] = Field(2.0, description="Speed in m/s", ge=0.1, le=10.0)
    yaw_speed: Optional[Union[float, Literal["sync"]]] = Field("sync", description="Yaw rotation speed in deg/s or 'sync'")

# class SafeReturnPlanRequestAddress(BaseModel):
#     address: str  # e.g., http://localhost:5000/WHMS/v1/safe_return_plan_request

class MissionPlanDTO(BaseModel):
    name: str = Field(default="unnamed", description="Logical mission name for identification", example="patrol_mission")
    id: Optional[str] = Field(default="", description="Unique mission ID (auto-generated if empty)", example="")
    config: Dict[str, Any] = Field(
        default_factory=lambda: {
            "joystick_mode": "ENABLED_ON_PAUSE",
            "mission_load_behavior": "QUEUE_IF_MISSION_IN_PROGRESS",
            "allow_duplicate_names": "ALLOW",
            "auto_start_behavior": "WAIT_FOR_COMMAND",
            "starting_point_behavior": "START_FROM_LANDING",
            "pause_behavior": "PAUSE_IMMEDIATELY",
            "successful_completion_behavior": "DEQUEUE_AND_IDLE",
            "unsuccessful_completion_behavior": "DEQUEUE_AND_IDLE"
        }, 
        description="Mission configuration - all fields optional with sensible defaults"
    )
    nodes: List[Node] = Field(..., description="List of mission steps/nodes")
    edges: List[Edge] = Field(..., description="Connections between mission steps/nodes")

    @model_validator(mode='after')
    def validate_unique_node_names(self) -> 'MissionPlanDTO':
        """Ensure all node names are unique."""
        names = [n.name for n in self.nodes]
        if len(names) != len(set(names)):
            duplicates = [name for name in names if names.count(name) > 1]
            raise ValueError(f"Duplicate node names found: {set(duplicates)}")
        return self

    @model_validator(mode='after')
    def validate_config(self) -> 'MissionPlanDTO':
        """Validate config dictionary against MissionConfig class."""
        try:
            MissionConfig.from_dict(self.config)
        except Exception as e:
            raise ValueError(f"Invalid mission config: {e}")
        return self

    @model_validator(mode='after')
    def validate_graph_integrity(self) -> 'MissionPlanDTO':
        """Ensure all edges reference existing nodes."""
        node_names = {n.name for n in self.nodes}
        for edge in self.edges:
            if edge.from_ not in node_names:
                raise ValueError(f"Edge references unknown source node: {edge.from_}")
            if edge.to not in node_names:
                raise ValueError(f"Edge references unknown target node: {edge.to}")
        return self
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "main",
                "config": {
                    "joystick_mode": "ENABLED_ON_PAUSE"
                },
                "nodes": [
                    {
                    "name": "Takeoff",
                    "type": "Takeoff",
                    "params": {
                        "alt": 1
                    }
                    },
                    {
                    "name": "Wait 1",
                    "type": "Wait",
                    "params": {
                        "duration": 2
                    }
                    },
                    {
                    "name": "GotoLocalWaypoint 1",
                    "type": "GotoLocalPosition",
                    "params": {
                        "waypoints": [
                        [
                            0.5,
                            0.0,
                            1.0
                        ]
                        ],
                        "yaws_deg": [
                        0.0
                        ],
                        "speed": [
                        0.2
                        ],
                        "yaw_speed": [
                        30.0
                        ]
                    }
                    },
                    {
                    "name": "GotoLocalWaypoint 2",
                    "type": "GotoLocalPosition",
                    "params": {
                        "waypoints": [
                        [
                            0.5,
                            0.5,
                            1.0
                        ],
                        [
                            0.0,
                            0.0,
                            1.0
                        ]
                        ],
                        "yaws_deg": [
                        0.0,
                        0.0
                        ],
                        "speed": [
                        0.2,
                        0.2
                        ],
                        "yaw_speed": [
                        30.0,
                        30.0
                        ]
                    }
                    },
                    {
                    "name": "GotoLocalWaypoint 3",
                    "type": "GotoLocalPosition",
                    "params": {
                        "waypoints": [
                        [
                            0.0,
                            0.5,
                            1.0
                        ],
                        [
                            0.5,
                            0.5,
                            1.0
                        ],
                        [
                            0.5,
                            0.0,
                            1.0
                        ]
                        ],
                        "yaws_deg": [
                        0.0,
                        10.0,
                        20.0
                        ],
                        "speed": [
                        0.2,
                        0.3,
                        0.4
                        ],
                        "yaw_speed": [
                        10.0,
                        20.0,
                        20.0
                        ]
                    }
                    },
                    {
                    "name": "Wait 2",
                    "type": "Wait",
                    "params": {
                        "duration": 2
                    }
                    },
                    {
                    "name": "Land",
                    "type": "Land",
                    "params": {}
                    }
                ],
                "edges": [
                    {
                    "from": "Takeoff",
                    "to": "Wait 1",
                    "condition": None
                    },
                    {
                    "from": "Wait 1",
                    "to": "GotoLocalWaypoint 1",
                    "condition": None
                    },
                    {
                    "from": "GotoLocalWaypoint 1",
                    "to": "GotoLocalWaypoint 2",
                    "condition": None
                    },
                    {
                    "from": "GotoLocalWaypoint 2",
                    "to": "GotoLocalWaypoint 3",
                    "condition": None
                    },
                    {
                    "from": "GotoLocalWaypoint 3",
                    "to": "Wait 2",
                    "condition": None
                    },
                    {
                    "from": "Wait 2",
                    "to": "Land",
                    "condition": None
                    }
                ]
            }
        }
    }

class CancelMissionRequest(BaseModel):
    action: Optional[Literal["NONE", "HOVER", "RETURN_TO_HOME", "LAND_IMMEDIATELY"]] = "HOVER"


class JoystickModeRequest(BaseModel):
    """Request model for setting joystick mode."""
    mode: Literal["DISABLED", "ENABLED_ALWAYS", "ENABLED_ON_PAUSE"]
    
    class Config:
        json_schema_extra = {
            "example": {
                "mode": "ENABLED_ON_PAUSE"
            }
        }


# ========================
# Redis Command Payloads
# ========================

class RedisCommandPayload(BaseModel):
    """Incoming Redis command message."""
    message_id: str
    command: str
    payload: Optional[Dict[str, Any]] = None


class RedisAckPayload(BaseModel):
    """Redis acknowledgment response."""
    message_id: Optional[str]
    command: str
    status: Literal["success", "error"]
    result: Optional[str] = None
    error: Optional[str] = None
    source: str = "petal-leafsdk"

    @classmethod
    def success(cls, message_id: Optional[str], command: str, result: str) -> "RedisAckPayload":
        return cls(message_id=message_id, command=command, status="success", result=result)

    @classmethod
    def failure(cls, message_id: Optional[str], command: str, error: str) -> "RedisAckPayload":
        return cls(message_id=message_id, command=command, status="error", error=error)


class RedisProgressPayload(BaseModel):
    """Mission progress update for Redis pub/sub."""
    message_id: str
    mission_id: str
    timestamp: float
    status: Dict[str, Any]
    source: str = "petal-leafsdk"


class RedisMissionLegPayload(BaseModel):
    """Mission leg update for Redis pub/sub."""
    message_id: str
    mission_id: str
    timestamp: float
    current_step_id: str
    previous_step_id: Optional[str] = None
    state: Optional[str] = None
    step_completed: Optional[bool] = None
    source: str = "petal-leafsdk"


# ========================
# MQTT Message Payloads
# ========================

class MQTTCommandMessage(BaseModel):
    """Incoming MQTT command message."""
    waitResponse: bool = Field(default=True, description="Whether to wait for a response")
    messageId: str = Field(..., description="Unique message ID")
    deviceId: str = Field(..., description="Device ID")
    command: str = Field(..., description="Command to execute")
    timestamp: str = Field(..., description="Timestamp of the message")
    payload: Dict[str, Any] = Field(..., description="Message payload")

    model_config = {
        "json_schema_extra": {
            "example": {
                "waitResponse": True,
                "messageId": "kkkss8fepn-1756665973142-bptyoj06z",
                "deviceId": "Instance-a92c5505-ccdb-4ac7-b0fe-74f4fa5fc5b9",
                "command": "petal-leafsdk/mission_plan",
                "payload": {
                    "mission_plan_json": {}
                },
                "timestamp": "2025-12-28T18:46:13.142Z"
            }
        }
    }


class MQTTResponseMessage(BaseModel):
    """Outgoing MQTT response message."""
    messageId: str = Field(..., description="Unique message ID matching the request")
    status: Literal["success", "error"] = Field(..., description="Response status")
    result: Optional[str] = Field(None, description="Success message")
    error: Optional[str] = Field(None, description="Error message")
    timestamp: Optional[str] = Field(None, description="Response timestamp")

    model_config = {
        "json_schema_extra": {
            "example": {
                "messageId": "kkkss8fepn-1756665973142-bptyoj06z",
                "status": "success",
                "result": "Mission accepted",
                "error": None,
                "timestamp": "2025-12-28T18:46:14.142Z"
            }
        }
    }