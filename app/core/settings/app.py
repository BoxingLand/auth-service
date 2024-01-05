
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

    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str
    REFRESH_TOKEN_EXPIRES_IN: int
    ACCESS_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str

    RABBITMQ_URL: str
    USER_CONFIRM_QUEUE_RECEIVE: str

    class Config:
        case_sensitive = True
        validate_assignment = True
        required = ['ASYNC_DATABASE_URI']
