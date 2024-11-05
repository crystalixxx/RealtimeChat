from http import HTTPStatus

from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from app.database.crud.user import get_user_by_id
from app.database.models import Chat, ChatMember, User
from app.database.schemas.chat import ChatUpdate
from app.database.session import get_db_connection
from app.misc.auth import get_current_user


def create_chat(
    db: Session, chat_name: str, user_creator_id: int, user_id: int
) -> Chat:
    chat = Chat(name=chat_name)

    db.add(chat)
    db.commit()
    db.refresh(chat)

    add_member_to_chat(db, chat.id, user_creator_id)
    add_member_to_chat(db, chat.id, user_id)

    return chat


def get_all_chats(db: Session) -> list[Chat]:
    return db.query(Chat).all()


def get_chat_by_id(db: Session, chat_id: int) -> Chat:
    return db.query(Chat).filter(Chat.id == chat_id).first()


def user_is_member_of_chat(
    chat_id: int, current_user=Depends(get_current_user), db=Depends(get_db_connection)
) -> ChatMember:
    user = get_user_by_id(db, current_user.id)
    if user.is_superadmin:
        return {}

    member = (
        db.query(ChatMember)
        .filter(ChatMember.chat_id == chat_id, ChatMember.member_id == current_user.id)
        .one_or_none()
    )

    if member is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not a member of chat"
        )

    return member


def add_member_to_chat(db: Session, chat_id: int, user_id: int) -> ChatMember:
    chat_member = ChatMember(chat_id=chat_id, member_id=user_id)

    db.add(chat_member)
    db.commit()
    db.refresh(chat_member)

    return chat_member


def get_users_to_add_to_chat(db: Session, chat_id: int) -> list[User]:
    subquery = (
        db.query(ChatMember.member_id).filter(ChatMember.chat_id == chat_id).subquery()
    )
    users = (
        db.query(User)
        .filter(User.id.notin_(select(subquery)), User.is_superadmin == False)
        .all()
    )

    return users


def get_members_of_chat(db: Session, chat_id: int) -> list[User]:
    subquery = (
        db.query(ChatMember.member_id).filter(ChatMember.chat_id == chat_id).subquery()
    )
    users = (
        db.query(User)
        .filter(User.id.in_(select(subquery)), User.is_superadmin == False)
        .all()
    )

    return users


def remove_member_from_chat(db: Session, chat_id: int, user_id: int) -> ChatMember:
    query = (
        db.query(ChatMember)
        .filter(ChatMember.chat_id == chat_id, ChatMember.member_id == user_id)
        .one()
    )

    db.delete(query)
    db.commit()

    return query


def delete_chat(db: Session, chat_id: int) -> Chat:
    chat = db.query(Chat).filter(Chat.id == chat_id).first()

    db.delete(chat)
    db.commit()

    return chat


def edit_chat(db: Session, chat_id: int, new_chat: ChatUpdate):
    chat = get_chat_by_id(db, chat_id)
    chat_dict = new_chat.model_dump(exclude_none=True)

    for key, value in chat_dict.items():
        setattr(chat, key, value)

    db.add(chat)
    db.commit()
    db.refresh(chat)

    return chat
