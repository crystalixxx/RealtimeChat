from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.backend.misc.security import get_hashed_password
from app.backend.database.schemas.user import UserCreate
from app.backend.database.models import User


def get_user_by_email(db: Session, user_email: str) -> User:
    user = db.query(User).filter(User.email == user_email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_hashed_password(user.password)

    user = User(
        username=user.username,
        email=user.email,
        is_blocked=user.is_blocked,
        hashed_password=hashed_password,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
