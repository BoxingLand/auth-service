from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Boxer(BaseModel):
    id: UUID
    weight: float
    height: float
    athletic_distinction: str
    user_id: UUID
    club_id: UUID
    updated_at: datetime
    created_at: datetime
    is_deleted: bool
