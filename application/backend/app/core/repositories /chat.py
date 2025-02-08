from .basics import SQLAlchemyRepository
from app.database.models import Chat


class ChatRepository(SQLAlchemyRepository):
    model = Chat
