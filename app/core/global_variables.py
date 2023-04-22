from typing import Dict, List, Optional

import schemas.command
from fastapi import WebSocket
from models.command import Command


class SocketManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = websocket
        else:
            await websocket.close(code=403, reason="Another client already listening.")

    async def disconnect(self, user_id: int, websocket: WebSocket):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def broadcast(self, command: Command):
        if command.receiver_id in self.active_connections:
            await self.active_connections[command.receiver_id].send_json(
                schemas.command.Command.from_orm(command).json(indent=2)
            )


socket_manager: Optional[SocketManager] = None


def init():
    global socket_manager
    socket_manager = SocketManager()
