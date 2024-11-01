from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)

    PG_CONNECTION_URL: str = "postgresql://admin:admin@postgres:5432/postgres"
    SECURITY_KEY: str = (
        "709cb22f047a59f492c4d6407e627240e2272bda11ab791c16fb4f4661f7285a95ba6efbc1bbf762cddcc3710a1487f4a3242f21b2d9cd751b3154a452c5a286"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379


config = Config()
