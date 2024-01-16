from datetime import date

from pydantic import BaseModel

from app.dto.models.user import AccountType


class ChangePasswordDto(BaseModel):
    current_password: str
    new_password: str
    new_password_confirm: str
    access_token: str


class AddRoleDto(BaseModel):
    account_type: AccountType
    access_token: str


class UpdateUserDto(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    birth_date: date | None = None
    country: str | None = None
    region: str | None = None
    city: str | None = None
    access_token: str | None = None
