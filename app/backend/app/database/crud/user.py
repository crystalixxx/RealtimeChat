from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from app.misc.security import get_hashed_password
from app.database.schemas.user import UserCreate, UserUpdate
from app.database.models import User, ChatMember


def get_all_users(db: Session) -> list[User]:
    return db.query(User).all()


def get_user_by_username(db: Session, user_name: str) -> User:
    user = db.query(User).filter(User.username == user_name).first()

    if not user:
        return None

    return user


def get_user_by_id(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return None

    return user


def create_user(db: Session, user: UserCreate) -> User:
    existing_user = get_user_by_username(db, user.username)
    if existing_user:
        return None

    hashed_password = get_hashed_password(user.password)

    user = User(
        username=user.username,
        is_superadmin=user.is_superadmin,
        is_blocked=user.is_blocked,
        hashed_password=hashed_password,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def delete_user(db: Session, user_id: int) -> None:
    user = get_user_by_id(db, user_id)

    if not user:
        return None

    db.delete(user)
    db.commit()

    return user


def update_user(db: Session, user_id: int, user: UserUpdate) -> User:
    old_user = get_user_by_id(db, user_id)

    if not old_user:
        return None

    dict_values = user.dict(exclude_unset=True)

    if "password" in dict_values:
        dict_values["hashed_password"] = get_hashed_password(user.password)
        del dict_values["password"]

    for key, value in dict_values.items():
        setattr(old_user, key, value)

    db.add(old_user)
    db.commit()
    db.refresh(old_user)

    return old_user


def block_user(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return None

    user.is_blocked = True
    db.commit()
    db.refresh(user)

    return user


def unblock_user(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return None

    user.is_blocked = False
    db.commit()
    db.refresh(user)

    return user
