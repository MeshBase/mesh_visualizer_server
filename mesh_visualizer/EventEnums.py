from enum import Enum


class EventType(str, Enum):
    CONNECT_NEIGHBOR = "connect"
    DISCONNECT_NEIGHBOR = "disconnect"
    HEARTBEAT = "heartbeat"
    TURNED_ON = "turned_on"
    TURNED_OFF = "turned_off"
    SEND_PACKET = "send_packet"
    RECIEVE_PACKET = "recieve_packet"
    DROP_PACKET = "drop_packet"
    UPDATE_GRAPH = "update_graph"
