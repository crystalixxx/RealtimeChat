from app.database.schemas.message import MessageCreate
from app.database.crud.messages import send_message

from fastapi import WebSocket
from sqlalchemy.orm import Session


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, chat_id: int, websocket: WebSocket):
        await websocket.accept()

        if chat_id not in self.active_connections:
            self.active_connections[chat_id] = []

        if websocket not in self.active_connections[chat_id]:
            self.active_connections[chat_id].append(websocket)

    def disconnect(self, chat_id: int, websocket: WebSocket):
        if chat_id in self.active_connections:
            self.active_connections[chat_id].remove(websocket)

    async def broadcast(self, user_id: int, chat_id: int, message: str, db: Session):
        struct_message = MessageCreate(
            sender_id=user_id, chat_id=chat_id, content=message
        )

        send_message(db, struct_message)

        for connection in self.active_connections[chat_id]:
            await connection.send_text(message)

    async def broadcast_delete(self, chat_id: int):
        for client in self.active_connections[chat_id]:
            await client.send_text("")


chat_manager = ConnectionManager()
