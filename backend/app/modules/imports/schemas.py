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


class ParsedImportRow(BaseModel):
    row_number: int = Field(ge=1)
    raw_date: str
    raw_task: str
    raw_category: str
    raw_time_spent_minutes: str
    raw_tags: str | None = None
    raw_notes: str | None = None


class NormalizedImportRow(BaseModel):
    row_number: int = Field(ge=1)
    log_date: date
    task_name: str
    normalized_task_name: str
    category_name: str
    normalized_category_name: str
    time_spent_minutes: int = Field(gt=0)
    tags: list[str] = Field(default_factory=list)
    note: str | None = None
    row_snapshot: dict[str, object] = Field(default_factory=dict)

    def to_api(self) -> dict[str, object]:
        return {
            "row_number": self.row_number,
            "date": self.log_date.isoformat(),
            "task": self.task_name,
            "category": self.category_name,
            "time_spent_minutes": self.time_spent_minutes,
            "tags": self.tags,
            "notes": self.note,
        }


class InvalidImportRow(BaseModel):
    row_number: int = Field(ge=1)
    reasons: list[str]
    row_snapshot: dict[str, object] = Field(default_factory=dict)

    @property
    def reason(self) -> str:
        return "; ".join(self.reasons)


class CSVParseResult(BaseModel):
    source_name: str
    total_rows: int = Field(ge=0)
    valid_rows: list[NormalizedImportRow] = Field(default_factory=list)
    invalid_rows: list[InvalidImportRow] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class ImportPreviewResponse(BaseModel):
    source_name: str
    total_rows: int = Field(ge=0)
    valid_row_count: int = Field(ge=0)
    invalid_row_count: int = Field(ge=0)
    valid_rows: list[dict[str, object]]
    invalid_rows: list[InvalidImportRow]
    warnings: list[str] = Field(default_factory=list)


class ConfirmedImportRequest(BaseModel):
    owner_id: UUID
    source_name: str
    csv_bytes: bytes = Field(repr=False)
    request_id: str | None = None
    idempotency_key: str | None = None


class ImportAcceptedResponse(BaseModel):
    import_run_id: UUID
    status: str


class ImportProcessingResult(BaseModel):
    import_run_id: UUID
    status: str
    processed_row_count: int = Field(ge=0)
    inserted_row_count: int = Field(ge=0)
    invalid_row_count: int = Field(ge=0)
    skipped_row_count: int = Field(ge=0)
    failed_row_count: int = Field(ge=0)
    failure_reason: str | None = None


class ImportRunStatus(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    source_type: str
    source_name: str
    status: str
    started_at: datetime | None = None
    completed_at: datetime | None = None
    processed_row_count: int
    inserted_row_count: int
    invalid_row_count: int
    skipped_row_count: int
    failed_row_count: int
    failure_reason: str | None = None


class ImportRowOutcomeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    import_run_id: UUID
    row_number: int | None = None
    outcome_type: str
    reason: str
    normalized_task_name: str | None = None
    log_date: date | None = None
    time_spent_minutes: int | None = None
    row_snapshot: dict[str, object] | None = None


class ImportRunPage(BaseModel):
    page: int
    limit: int
    total: int
    items: list[ImportRunStatus]


class ImportRowOutcomePage(BaseModel):
    page: int
    limit: int
    total: int
    items: list[ImportRowOutcomeRead]
