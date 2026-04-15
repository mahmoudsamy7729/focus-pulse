from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class NoteCreate(BaseModel):
    owner_id: UUID
    task_id: UUID
    content: str | None = None
    import_run_id: UUID | None = None


class NoteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    owner_id: UUID
    task_id: UUID
    content: str
    import_run_id: UUID | None = None
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
