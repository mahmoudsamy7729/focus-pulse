from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AIInsightRunCreate(BaseModel):
    owner_id: UUID
    target_period_type: str
    period_start: date
    period_end: date
    source_daily_log_ids: list[UUID]


class AIInsightRunRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    owner_id: UUID
    target_period_type: str
    period_start: date
    period_end: date
    status: str
    source_summary: dict[str, object]
    output_summary: dict[str, object] | None = None
    failure_reason: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
