import datetime
from pydantic import BaseModel
from typing import Optional
from mesh_visualizer.EventEnums import EventType
from mesh_visualizer.TechnologiesEnums import TechnologyTypes


class InputEventModel(BaseModel):
    event_type: EventType
    source_id: str
    timestamp: Optional[str] = datetime.datetime.now().isoformat()


class ConnectNeighborInput(InputEventModel):
    event_type: EventType = EventType.CONNECT_NEIGHBOR
    neighbor_id: str
    technology: TechnologyTypes


class DisconnectNeighborInput(InputEventModel):
    event_type: EventType = EventType.DISCONNECT_NEIGHBOR
    neighbor_id: str
    technology: TechnologyTypes


class HeartbeatInput(InputEventModel):
    event_type: EventType = EventType.HEARTBEAT
    destination_id: str
    packet_id: str
    technology: TechnologyTypes


class TurnedOnInput(InputEventModel):
    event_type: EventType = EventType.TURNED_ON


class TurnedOffInput(InputEventModel):
    event_type: EventType = EventType.TURNED_OFF


class SendPacketInput(InputEventModel):
    event_type: EventType = EventType.SEND_PACKET
    destination_id: str
    packet_id: str
    technology: TechnologyTypes


class RecievePacketInput(InputEventModel):
    event_type: EventType = EventType.RECIEVE_PACKET
    destination_id: str
    packet_id: str
    technology: TechnologyTypes


class DropPacketInput(InputEventModel):
    event_type: EventType = EventType.DROP_PACKET
    packet_id: str
    reason: Optional[str] = "Unspecified reason for dropping the packet"
