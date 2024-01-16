from datetime import date, datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class AccountType(str, Enum):
    BOXER = "boxer"
    COACH = "coach"
    JUDE = "judge"
    ORGANIZER = "organizer"


class User(BaseModel):
    id: UUID
    email: str | None = None
    password: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    phone_number: str | None = None
    birthdate: date | None = None
    country: str | None = None
    region: str | None = None
    city: str | None = None
    updated_at: datetime
    created_at: datetime
    is_active: bool
    is_deleted: bool


class UserDto(BaseModel):
    id: UUID
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    phone_number: str | None = None
    birth_date: date | None = None
    country: str | None = None
    region: str | None = None
    city: str | None = None
