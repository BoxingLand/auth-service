from pydantic import BaseModel, EmailStr

from app.dto.request.signup_dto import AccountType


class SigninRequestDto(BaseModel):
    email: EmailStr | None = None
    phone_number: str | None = None
    password: str
