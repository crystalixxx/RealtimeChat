import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.database.session import get_db_connection
from app.misc.auth import (
    sign_up_new_user,
    authenticate_user,
    get_current_superuser,
    get_current_user,
)
from app.misc.config import config
from app.misc.security import create_access_token

auth_router = APIRouter()


@auth_router.post("/login")
async def login(
    db=Depends(get_db_connection), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = datetime.timedelta(
        minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    access_token = create_access_token(
        data={"sub": user.username, "permissions": "user"},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/signup")
async def signup(
    db=Depends(get_db_connection), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = sign_up_new_user(form_data.username, form_data.password, False, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = datetime.timedelta(
        minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    access_token = create_access_token(
        data={"sub": user.username, "permissions": "user"},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/signup_superadmin")
async def signup_superadmin(
    db=Depends(get_db_connection),
    form_data: OAuth2PasswordRequestForm = Depends(),
    current_user=Depends(get_current_superuser),
):
    user = sign_up_new_user(form_data.username, form_data.password, True, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )


@auth_router.get("/check-auth")
async def check_auth(user=Depends(get_current_user)):
    return {
        "status": "ok",
        "username": user.username,
        "id": user.id,
        "is_superadmin": user.is_superadmin,
    }
