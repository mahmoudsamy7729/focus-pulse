from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, Index, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from app.core.database import Base
from app.shared.enums.run_status import RunStatus
from app.shared.models.base import SoftDeleteMixin, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.modules.notes.models import Note
    from app.modules.tasks.models import Task


class ImportRun(UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "import_runs"
    __table_args__ = (
        CheckConstraint("processed_row_count >= 0", name="ck_import_runs_processed_non_negative"),
        CheckConstraint("inserted_row_count >= 0", name="ck_import_runs_inserted_non_negative"),
        CheckConstraint("invalid_row_count >= 0", name="ck_import_runs_invalid_non_negative"),
        CheckConstraint("skipped_row_count >= 0", name="ck_import_runs_skipped_non_negative"),
        CheckConstraint("failed_row_count >= 0", name="ck_import_runs_failed_non_negative"),
    )

    owner_id: Mapped[UUID] = mapped_column(Uuid, nullable=False, index=True)
    source_type: Mapped[str] = mapped_column(String(32), nullable=False, default="csv")
    source_name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default=RunStatus.PENDING.value, index=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    processed_row_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    inserted_row_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    invalid_row_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    skipped_row_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    failed_row_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    failure_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    tasks: Mapped[list[Task]] = relationship("Task", back_populates="import_run")
    notes: Mapped[list[Note]] = relationship("Note", back_populates="import_run")
    row_outcomes: Mapped[list[ImportRowOutcome]] = relationship(
        "ImportRowOutcome",
        back_populates="import_run",
        cascade="all, delete-orphan",
    )


Index("ix_import_runs_owner_status_created", ImportRun.owner_id, ImportRun.status, ImportRun.created_at)


class ImportRowOutcome(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "import_row_outcomes"
    __table_args__ = (Index("ix_import_row_outcomes_run_type", "import_run_id", "outcome_type"),)

    owner_id: Mapped[UUID] = mapped_column(Uuid, nullable=False, index=True)
    import_run_id: Mapped[UUID] = mapped_column(ForeignKey("import_runs.id"), nullable=False, index=True)
    row_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    outcome_type: Mapped[str] = mapped_column(String(32), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    normalized_task_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    log_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    time_spent_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    row_snapshot: Mapped[dict[str, object] | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    import_run: Mapped[ImportRun] = relationship("ImportRun", back_populates="row_outcomes")
