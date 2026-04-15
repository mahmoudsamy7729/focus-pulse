from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ImportRunCreate(BaseModel):
    owner_id: UUID
    source_type: str = "csv"
    source_name: str


class ImportRunRead(ImportRunCreate):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: str
    started_at: datetime | None = None
    completed_at: datetime | None = None
    processed_row_count: int
    inserted_row_count: int
    invalid_row_count: int
    skipped_row_count: int
    failed_row_count: int
    failure_reason: str | None = None
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None


class ImportRowOutcomeCreate(BaseModel):
    import_run_id: UUID
    row_number: int | None = Field(default=None, ge=1)
    outcome_type: str
    reason: str
    normalized_task_name: str | None = None
    log_date: date | None = None
    time_spent_minutes: int | None = Field(default=None, gt=0)
    row_snapshot: dict[str, object] | None = None
