from enum import Enum

from pydantic import BaseModel, EmailStr


class AccountType(str, Enum):
    BOXER = "boxer"
    COACH = "coach"
    JUDE = "judge"
    ORGANIZER = "organizer"


class SignupDto(BaseModel):
    account_type: AccountType
    phone_number: str | None = None
    email: EmailStr | None = None
    password: str
    password_confirm: str

    # class Config:
    #     hashed_password = None
