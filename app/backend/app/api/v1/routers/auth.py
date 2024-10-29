import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.backend.app.database.session import get_db_connection
from app.backend.app.misc.auth import sign_up_new_user
from app.backend.app.misc.config import config
from app.backend.app.misc.security import create_access_token

auth_router = APIRouter()


@auth_router.post("/signup")
async def signup(
    db=Depends(get_db_connection), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = sign_up_new_user(form_data.username, form_data.password, db)

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
        data={"sub": user.email, "permissions": "user"},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}
