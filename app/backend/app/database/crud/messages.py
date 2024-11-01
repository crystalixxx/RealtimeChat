from sqlalchemy.orm import Session

from app.database.models import Chat, Message


def send_message(db: Session, user_id: int, chat_id: int, message: str):
    message = Message(sender_id=user_id, chat_id=chat_id, content=message)

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def get_messages_from_chat(db: Session, chat_id: int):
    messages = db.query(Message).filter(Message.chat_id == chat_id).all()
    return messages
