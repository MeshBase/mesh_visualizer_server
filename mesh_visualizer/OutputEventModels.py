# Output Models (with timestamp)
import datetime
from typing import Mapping, Optional
from pydantic import BaseModel

from mesh_visualizer.EventEnums import EventType
from mesh_visualizer.InputEventsModels import TechnologyTypes


class OutputEventModel(BaseModel):
    event_type: EventType
    timestamp: str = datetime.datetime.now().isoformat()


class ConnectNeighborOutput(OutputEventModel):
    event_type: EventType = EventType.CONNECT_NEIGHBOR
    node_id: str
    neighbor_id: str
    technology: TechnologyTypes
    graph: Mapping


class DisconnectNeighborOutput(OutputEventModel):
    event_type: EventType = EventType.DISCONNECT_NEIGHBOR
    node_id: str
    neighbor_id: str
    graph: Mapping


class HeartbeatOutput(OutputEventModel):
    event_type: EventType = EventType.HEARTBEAT
    packet_id: str
    node_id: str


class TurnedOnOutput(OutputEventModel):
    event_type: EventType = EventType.TURNED_ON
    node_id: str


class TurnedOffOutput(OutputEventModel):
    event_type: EventType = EventType.TURNED_OFF
    node_id: str


class SendPacketOutput(OutputEventModel):
    event_type: EventType = EventType.SEND_PACKET
    node_id: str
    destination_id: str
    packet_id: str
    technology: TechnologyTypes


class RecievePacketOutput(OutputEventModel):
    event_type: EventType = EventType.RECIEVE_PACKET
    node_id: str
    source_id: str
    packet_id: str
    technology: TechnologyTypes


class DropPacketOutput(OutputEventModel):
    event_type: EventType = EventType.DROP_PACKET
    node_id: str
    packet_id: str
    reason: Optional[str] = None


class UpdateGraphOutput(OutputEventModel):
    event_type: EventType = EventType.UPDATE_GRAPH
    graph: Mapping
