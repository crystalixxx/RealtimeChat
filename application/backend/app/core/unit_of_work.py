from fastapi import Depends

from core.interfaces import AbstractUnitOfWork
from app.core.repositories import ChatRepository
from core.repositories import UserRepository, MessageRepository
from database.session import get_db_connection


class SQLAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(
            self,
            session_factory=Depends(get_db_connection)
    ):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = next(self.session_factory)

        self.chats = ChatRepository
        self.users = UserRepository
        self.message = MessageRepository

        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type:
                await self.rollback()
            else:
                await self.commit()
        finally:
            if self.session:
                await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
