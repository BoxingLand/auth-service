
from pydantic import AnyHttpUrl

from app.core.settings.base import BaseAppSettings


class AppSettings(BaseAppSettings):
    API_PREFIX: str = "/api"
    API_TITLE: str
    CORS_ORIGINS: list[str] | list[AnyHttpUrl]
    APP_PORT: int | str

    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: int | str
    DATABASE_NAME: str

    DB_POOL_SIZE: int = 90

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    JWT_ALGORITHM: str
    ENCRYPT_KEY: str

    MAIL_FROM: str
    MAIL_PASSWORD: str
    MAIL_PORT: int
    MAIL_SERVER: str

    class Config:
        case_sensitive = True
        validate_assignment = True
