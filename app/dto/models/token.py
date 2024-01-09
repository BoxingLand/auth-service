from uuid import UUID

from pydantic import BaseModel


class Token(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str

class RefreshTokenDto(BaseModel):
    user_id: UUID
    refresh_token: str
