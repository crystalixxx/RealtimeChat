from pydantic_settings import BaseSettings


class Config(BaseSettings):
    PG_CONNECTION_URL: str
    SECURITY_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


config = Config()
