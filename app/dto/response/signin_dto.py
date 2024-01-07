from pydantic import BaseModel


class SigninResponseDto(BaseModel):
    access_token: str
    refresh_token: str
