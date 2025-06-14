from typing import Set
from fastapi import WebSocket
from mesh_visualizer.OutputEventModels import OutputEventModel


class ClientConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, websocket: WebSocket, event: OutputEventModel):
        if websocket in self.active_connections:
            await websocket.send_json(event.model_dump_json())

    async def broadcastEvent(self, event: OutputEventModel):
        for connection in self.active_connections:
            await connection.send_json(event.model_dump_json())
