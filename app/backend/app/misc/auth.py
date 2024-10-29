import jwt

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.backend.app.database.crud.user import create_user, get_user_by_email
from app.backend.app.database.session import get_db_connection
from app.backend.app.database.schemas.user import UserCreate, User
from app.backend.app.misc.security import oauth2_scheme
from app.backend.app.misc.config import config


async def get_current_user(
    db=Depends(get_db_connection), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, config.SECURITY_KEY, algorithms=[config.ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise credentials_exception
    except:
        raise credentials_exception

    user = get_user_by_email(db, email)
    if user is None:
        raise credentials_exception

    return user


async def get_current_superuser(current_user: User = Depends(get_current_user)):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have enough permissions. Access is denied",
        )

    return current_user


def sign_up_new_user(email: str, password: str, db: Session):
    user = get_user_by_email(db, email)
    if user:
        return False

    new_user = create_user(
        db, UserCreate(email=email, password=password, is_superuser=False)
    )

    return new_user
