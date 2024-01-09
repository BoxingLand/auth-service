from pydantic import BaseModel


class ChangePasswordDto(BaseModel):
    current_password: str
    new_password: str
    new_password_confirm: str
    access_token: str
