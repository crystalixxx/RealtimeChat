from sqlalchemy.orm import Session

from app.database.models import Chat, Message
from app.database.schemas.message import MessageCreate


async def get_message_by_id(db: Session, message_id: int):
    return db.query(Message).filter(Message.id == message_id).one_or_none()


def send_message(db: Session, message: MessageCreate):
    message = Message(
        sender_id=message.sender_id, chat_id=message.chat_id, content=message.content
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def get_messages_from_chat(
    db: Session, chat_id: int, limit: int = 100, offset: int = 0
):
    messages = (
        db.query(Message)
        .filter(Message.chat_id == chat_id)
        .order_by(Message.sent_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )
    return messages


def delete_message(db: Session, message_id: int):
    message = db.query(Message).filter(Message.id == message_id).one()

    db.delete(message)
    db.commit()

    return message
