from enum import Enum

from pydantic import BaseModel, EmailStr


class AccountType(str, Enum):
    BOXER = "boxer"
    COACH = "coach"
    JUDE = "judge"
    SPAN_ENTITY = "SpanEntity"


class SignupDto(BaseModel):
    account_type: AccountType
    phone_number: str | None
    email: EmailStr | None
    password: str

    class Config:
        hashed_password = None
