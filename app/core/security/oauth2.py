import base64
from typing import List

from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel

from app.core.config import settings


class Settings(BaseModel):
    auth_jwt_algorithm: str = settings.JWT_ALGORITHM
    auth_jwt_decode_algorithms: List[str] = [settings.JWT_ALGORITHM]
    auth_jwt_token_location: set = {'cookies', 'headers'}
    auth_jwt_access_cookie_key: str = 'access_token'
    auth_jwt_refresh_cookie_key: str = 'refresh_token'
    auth_jwt_cookie_csrf_protect: bool = False
    auth_jwt_public_key: str = base64.b64decode(
        settings.JWT_PUBLIC_KEY).decode('utf-8')
    auth_jwt_private_key: str = base64.b64decode(
        settings.JWT_PRIVATE_KEY).decode('utf-8')


@AuthJWT.load_config
def get_config():
    return Settings()
