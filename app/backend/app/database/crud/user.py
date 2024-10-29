from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.misc.security import get_hashed_password
from app.database.schemas.user import UserCreate
from app.database.models import User


def get_user_by_username(db: Session, user_name: str) -> User:
    user = db.query(User).filter(User.username == user_name).first()

    if not user:
        return None

    return user


def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_hashed_password(user.password)

    user = User(
        username=user.username,
        is_blocked=user.is_blocked,
        hashed_password=hashed_password,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
