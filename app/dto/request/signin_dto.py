from pydantic import BaseModel, EmailStr


class SigninRequestDto(BaseModel):
    email: EmailStr | None = None
    phone_number: str | None = None
    password: str
