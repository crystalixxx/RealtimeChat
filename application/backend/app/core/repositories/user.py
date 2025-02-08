from .basics import SQLAlchemyRepository
from app.database.models import User


class UserRepository(SQLAlchemyRepository):
    model = User
