import datetime
import jwt

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from app.misc.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(*, data: dict, expires_delta: datetime.timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(tz=datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECURITY_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt
