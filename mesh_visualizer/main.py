from typing import Union
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import networkx as nx
from mesh_visualizer import *

app = FastAPI(
    title="Mesh Visualizer API",
    description="API for visualizing 3D meshes",
    version="1.0.0",
    openapi_tags=[
        {"name": "Mesh", "description": "Operations related to 3D mesh visualization"}
    ],
)

graph = nx.MultiGraph()
manager = ClientConnectionManager()


@app.get("/health", tags=["Mesh"])
async def health_check():
    return {"status": "healthy"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        data = nx.node_link_data(graph)
        await manager.send_message(
            websocket,
            UpdateGraphOutput(graph=data),
        )

        # keep connection alive
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect as e:
        print(f"WebSocket disconnected: {e}")

    except Exception as e:
        print(f"WebSocket error: {e}")

    finally:
        await manager.disconnect(websocket)


@app.post("/event", tags=["Mesh"], response_model=OutputEventModel)
async def handle_event(
    event: Union[
        ConnectNeighborInput,
        DisconnectNeighborInput,
        HeartbeatInput,
        TurnedOnInput,
        TurnedOffInput,
        SendPacketInput,
        RecievePacketInput,
        DropPacketInput,
    ],
) -> OutputEventModel:
    """Broadcast an event to all connected clients and update the graph accordingly."""
    try:
        _output_event = None
        print(event)
        if event.event_type == EventType.CONNECT_NEIGHBOR:
            _event = ConnectNeighborInput.model_validate(event.model_dump())
            graph.add_node(_event.source_id)
            graph.add_node(_event.neighbor_id)
            graph.add_edge(
                event.source_id,
                _event.neighbor_id,
                technology=_event.technology,
                key=_event.technology,
            )
            _output_event = ConnectNeighborOutput(
                node_id=_event.source_id,
                neighbor_id=_event.neighbor_id,
                technology=_event.technology,
                graph=nx.node_link_data(graph),
            )
            await manager.broadcastEvent(_output_event)

        elif event.event_type == EventType.DISCONNECT_NEIGHBOR:
            _event = DisconnectNeighborInput.model_validate(event.model_dump())

            # Get all edges between source and neighbor
            edges_between = list(
                graph.get_edge_data(_event.source_id, _event.neighbor_id).items()
            )

            # Find and remove the one with matching technology
            for key, edge_attrs in edges_between:
                if edge_attrs.get("technology") == _event.technology:
                    graph.remove_edge(_event.source_id, _event.neighbor_id, key)
                    break

            _output_event = DisconnectNeighborOutput(
                node_id=_event.source_id,
                neighbor_id=_event.neighbor_id,
                technology=_event.technology,
                graph=nx.node_link_data(graph),
            )
            await manager.broadcastEvent(_output_event)

        elif event.event_type == EventType.HEARTBEAT:
            _event = HeartbeatInput.model_validate(event.model_dump())
            if not graph.has_node(_event.source_id):
                graph.add_node(_event.source_id)

            _output_event = HeartbeatOutput(
                node_id=_event.source_id,
                packet_id=_event.packet_id,
                destination_id=_event.destination_id,
                technology=_event.technology,
            )
            await manager.broadcastEvent(_output_event)

        elif event.event_type == EventType.TURNED_ON:
            _event = TurnedOnInput.model_validate(event.model_dump())
            if not graph.has_node(event.source_id):
                graph.add_node(event.source_id)

            _output_event = TurnedOnOutput(
                node_id=_event.source_id,
                graph=nx.node_link_data(graph),
            )
            await manager.broadcastEvent(_output_event)

        elif event.event_type == EventType.TURNED_OFF:
            _event = TurnedOnInput.model_validate(event.model_dump())
            if graph.has_node(event.source_id):
                graph.remove_node(event.source_id)

            _output_event = TurnedOffOutput(
                node_id=_event.source_id, graph=nx.node_link_data(graph)
            )
            await manager.broadcastEvent(_output_event)

        elif event.event_type == EventType.SEND_PACKET:
            _event = SendPacketInput.model_validate(event.model_dump())

            if not graph.has_node(_event.source_id):
                graph.add_node(_event.source_id)

            _output_event = SendPacketOutput(
                node_id=_event.source_id,
                destination_id=_event.destination_id,
                packet_id=_event.packet_id,
                technology=_event.technology,
            )
            await manager.broadcastEvent(_output_event)

        elif event.event_type == EventType.RECIEVE_PACKET:
            _event = RecievePacketInput.model_validate(event.model_dump())

            if not graph.has_node(_event.destination_id):
                graph.add_node(_event.destination_id)

            _output_event = RecievePacketOutput(
                node_id=_event.destination_id,
                packet_id=_event.packet_id,
                technology=_event.technology,
            )

            await manager.broadcastEvent(_output_event)

        elif event.event_type == EventType.DROP_PACKET:
            _event = DropPacketInput.model_validate(event.model_dump())

            if not graph.has_node(_event.source_id):
                graph.add_node(_event.source_id)

            _output_event = DropPacketOutput(
                node_id=_event.source_id,
                packet_id=_event.packet_id,
                reason=_event.reason,
            )
            await manager.broadcastEvent(_output_event)

        else:
            raise ValueError(f"Unknown event type: {event.event_type}")

        return _output_event

    except Exception as e:
        print(f"Error handling event: {e}")
        raise ValueError(f"Failed to handle event: {e}")
