from sqlalchemy.orm import Session

from app.database.models import Chat
from app.database.schemas.chat import ChatCreate


def create_chat(db: Session, chat: ChatCreate) -> Chat:
    chat = Chat(name=chat.name)

    db.add(chat)
    db.commit()
    db.refresh(chat)

    return chat
