from sqlalchemy.orm import Session

from app.database.models import Chat as ModelsChat, ChatMember
from app.database.schemas.chat import ChatCreate, Chat


def create_chat(
    db: Session, chat_name: str, user_creator_id: int, user_id: int
) -> ModelsChat:
    chat = ModelsChat(name=chat_name)

    db.add(chat)
    db.commit()
    db.refresh(chat)

    add_member_to_chat(db, chat, user_creator_id)
    add_member_to_chat(db, chat, user_id)

    return chat


def add_member_to_chat(db: Session, chat: Chat, user_id: int) -> ChatMember:
    chat_member = ChatMember(chat_id=chat.id, member_id=user_id)

    db.add(chat_member)
    db.commit()
    db.refresh(chat_member)

    return chat_member
