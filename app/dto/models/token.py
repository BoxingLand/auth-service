from pydantic import BaseModel

from app.dto.models.user import User


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    user: User
