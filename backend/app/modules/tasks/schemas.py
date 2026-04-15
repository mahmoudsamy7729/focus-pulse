from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CategoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    owner_id: UUID
    name: str
    normalized_name: str
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None


class TaskCreate(BaseModel):
    owner_id: UUID
    daily_log_id: UUID
    title: str
    time_spent_minutes: int = Field(gt=0)
    category_name: str
    tags: list[str] = Field(default_factory=list)
    note: str | None = None
    import_run_id: UUID | None = None


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    owner_id: UUID
    daily_log_id: UUID
    category_id: UUID
    title: str
    normalized_title: str
    time_spent_minutes: int
    tags: list[str]
    source: str
    import_run_id: UUID | None = None
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
