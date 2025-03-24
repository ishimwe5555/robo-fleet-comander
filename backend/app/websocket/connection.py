from fastapi import WebSocket
from typing import Dict, Set
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast_robot_position(self, robot_id: str, position: Dict):
        message = {
            "type": "position_update",
            "robot_id": robot_id,
            "position": position
        }
        await self.broadcast(json.dumps(message))

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                # Connection might be closed
                self.active_connections.remove(connection)

manager = ConnectionManager() 