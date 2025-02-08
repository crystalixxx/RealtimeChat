from .basics import SQLAlchemyRepository
from app.database.models import Message


class MessageRepository(SQLAlchemyRepository):
    model = Message
