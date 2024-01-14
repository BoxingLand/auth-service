from datetime import date

from pydantic import BaseModel


class UpdateUserDto(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    birth_date: date
    country: str
    region: str
    city: str
    access_token: str
