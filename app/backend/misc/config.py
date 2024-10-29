from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DATABASE_URL: str
    DATABASE_HOST: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_PORT: str
    SECURITY_KEY: str = (
        "709cb22f047a59f492c4d6407e627240e2272bda11ab791c16fb4f4661f7285a95ba6efbc1bbf762cddcc3710a1487f4a3242f21b2d9cd751b3154a452c5a286"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    def pg_connection_url(self):
        return f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"


config = Config()
