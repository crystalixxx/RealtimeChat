from datetime import datetime

from pydantic import EmailStr
from sqlalchemy import (
    Integer,
    Column,
    String,
    ForeignKey,
    DateTime,
    func,
    Text,
    Boolean,
)
from sqlalchemy.orm import declarative_base, Mapped, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    username: str = Column(String, nullable=False, unique=True)
    hashed_password: str = Column(String, nullable=False)
    is_blocked: bool = Column(Boolean, nullable=False, default=False)
    is_superadmin: bool = Column(Boolean, nullable=False, default=False)

    chats: Mapped[list["Chat"]] = relationship(
        "Chat", secondary="chat_member", back_populates="users", lazy="joined"
    )
    messages: Mapped[list["Message"]] = relationship("Message", back_populates="sender")


class Chat(Base):
    __tablename__ = "chat"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String, nullable=False)
    created_at: datetime = Column(DateTime(timezone=True), server_default=func.now())

    users: Mapped[list["User"]] = relationship(
        "User", secondary="chat_member", back_populates="chats", lazy="joined"
    )


class Message(Base):
    __tablename__ = "message"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    sender_id: int = Column(Integer, ForeignKey("user.id"), nullable=False)
    chat_id: int = Column(Integer, ForeignKey("chat.id"), nullable=False)
    content: str = Column(Text, nullable=False)
    sent_at: datetime = Column(DateTime(timezone=True), server_default=func.now())

    sender = relationship("User", back_populates="messages", lazy="joined")


class ChatMember(Base):
    __tablename__ = "chat_member"

    chat_id: int = Column(
        Integer, ForeignKey("chat.id"), nullable=False, primary_key=True
    )
    member_id: int = Column(
        Integer, ForeignKey("user.id"), nullable=False, primary_key=True
    )
