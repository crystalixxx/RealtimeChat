import jwt

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.database.crud.user import create_user, get_user_by_username
from app.database.session import get_db_connection
from app.database.schemas.user import UserCreate, User
from app.misc.security import oauth2_scheme, verify_password
from app.misc.config import settings


async def get_current_user(
    db=Depends(get_db_connection), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECURITY_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise credentials_exception
    except:
        raise credentials_exception

    user = get_user_by_username(db, email)
    if user is None:
        raise credentials_exception

    return user


async def get_current_superuser(current_user: User = Depends(get_current_user)):
    if not current_user.is_superadmin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have enough permissions. Access is denied",
        )

    return current_user


def authenticate_user(username: str, password: str, db):
    user = get_user_by_username(db, username)

    if not user:
        return False

    if not verify_password(password, user.hashed_password):
        return False

    return user


def sign_up_new_user(username: str, password: str, is_admin: bool, db: Session):
    user = get_user_by_username(db, username)
    if user:
        return False

    new_user = create_user(
        db, UserCreate(username=username, password=password, is_superadmin=is_admin)
    )

    return new_user
