import redis

from fastapi import WebSocket
from sqlalchemy.orm import Session

from app.misc.config import config
from app.database.models import Message

redis_client = redis.Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    decode_responses=True,
)

import json
from typing import Dict, List
from fastapi import WebSocket
from sqlalchemy.orm import Session


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, List[WebSocket]] = {}

    async def connect(self, chat_id: int, websocket: WebSocket):
        await websocket.accept()

        if chat_id not in self.active_connections:
            self.active_connections[chat_id] = []

        if websocket not in self.active_connections[chat_id]:
            self.active_connections[chat_id].append(websocket)

    def disconnect(self, chat_id: int, websocket: WebSocket):
        if chat_id in self.active_connections:
            self.active_connections[chat_id].remove(websocket)

    @staticmethod
    def save_message_to_db(chat_id: int, sender_id: int, content: str, db: Session):
        new_message = Message(
            sender_id=sender_id,
            chat_id=chat_id,
            content=content,
        )
        db.add(new_message)
        db.commit()

    async def broadcast(self, user_id: int, chat_id: int, message: str, db: Session):
        self.save_message_to_db(chat_id, user_id, message, db)

        for connection in self.active_connections[chat_id]:
            await connection.send_text(message)


chat_manager = ConnectionManager()
