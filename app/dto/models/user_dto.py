from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel


class UserDTO(BaseModel):
    id: UUID
    email: str
    password: str
    first_name: str
    last_name: str
    middle_name: str
    phone_number: str
    registration_date: datetime
    birth_date: date
    country: str
    region: str
    city: str
    is_active: bool
    updated_at: datetime
    created_at: datetime
