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


class ConnectionManager:
    def __init__(self, new_redis_client, prefix_id):
        self.redis_client = new_redis_client
        self.prefix_id = prefix_id

    async def connect(self, chat_id: str, user_id: str):
        self.redis_client.sadd(f"{self.prefix_id}:{chat_id}", user_id)

    def disconnect(self, chat_id: str, user_id: str):
        self.redis_client.srem(f"{self.prefix_id}:{chat_id}", user_id)

    async def send_message(
        self, chat_id: int, message: str, sender_id: int, db: Session
    ):
        self.redis_client.publish(chat_id, message)
        self.save_message_to_db(chat_id, sender_id, message, db)

    async def listen_to_messages(self, chat_id: str, websocket: WebSocket):
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe(chat_id)

        for message in pubsub.listen():
            if message["type"] == "message":
                await websocket.send_text(message["data"])

    @staticmethod
    def save_message_to_db(chat_id: int, sender_id: int, content: str, db: Session):
        new_message = Message(
            sender_id=sender_id,
            chat_id=chat_id,
            content=content,
        )
        db.add(new_message)
        db.commit()


chat_manager = ConnectionManager(redis_client, "CHAT_CONNECTION")
