from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.modules.analytics.schemas import EmptyState


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


class TaskTimelineItem(BaseModel):
    id: UUID
    title: str
    time_spent_minutes: int
    display_time: str
    category: str
    tags: list[str]
    note: str | None = None
    source: str
    timeline_position: int


class DayDetail(BaseModel):
    date: date
    total_minutes: int
    display_total: str
    task_count: int
    tasks: list[TaskTimelineItem]
    empty_state: EmptyState | None = None
