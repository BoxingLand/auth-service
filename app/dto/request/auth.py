
from pydantic import BaseModel, EmailStr

from app.dto.models.user import AccountType


class SigninRequestDto(BaseModel):
    email: EmailStr | None = None
    phone_number: str | None = None
    password: str


class SignupRequestDto(BaseModel):
    account_type: AccountType
    phone_number: str | None = None
    email: EmailStr | None = None
    password: str
    password_confirm: str
