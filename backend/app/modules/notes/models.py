from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Index, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from app.core.database import Base
from app.shared.models.base import SoftDeleteMixin, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.modules.imports.models import ImportRun
    from app.modules.tasks.models import Task


class Note(UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "notes"

    owner_id: Mapped[UUID] = mapped_column(Uuid, nullable=False, index=True)
    task_id: Mapped[UUID] = mapped_column(ForeignKey("tasks.id"), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    import_run_id: Mapped[UUID | None] = mapped_column(ForeignKey("import_runs.id"), nullable=True, index=True)

    task: Mapped[Task] = relationship("Task", back_populates="note")
    import_run: Mapped[ImportRun | None] = relationship("ImportRun", back_populates="notes")


Index(
    "ix_notes_one_active_per_task",
    Note.task_id,
    unique=True,
    sqlite_where=Note.deleted_at.is_(None),
    postgresql_where=Note.deleted_at.is_(None),
)
