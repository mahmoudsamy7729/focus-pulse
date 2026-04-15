from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DailyLogBase(BaseModel):
    owner_id: UUID
    log_date: date
    source: str = "manual"


class DailyLogCreate(DailyLogBase):
    pass


class DailyLogRead(DailyLogBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
