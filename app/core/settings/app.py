from app.core.settings.base import BaseAppSettings


class AppSettings(BaseAppSettings):
    DATABASE_USER: str = "admin"
    DATABASE_PASSWORD: str = "admin"
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int | str = "2345"
    DATABASE_NAME: str = "auth"

    DB_POOL_SIZE: int = 90

    SERVER_PORT: int = 50052

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 129990
    JWT_ALGORITHM: str = "HS256"
    ENCRYPT_KEY: str = "TshgGacKPYrm35m89UqbRg46JAbUm2yRtxOCQFdqa3w="

    MAIL_FROM: str = "mrgladiolus56@gmail.com"
    MAIL_PASSWORD: str = "qpgoanfykibjbyus"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"


    class Config:
        case_sensitive = True
        validate_assignment = True
