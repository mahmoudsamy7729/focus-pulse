from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from app.core.database import Base
from app.shared.enums.source import DEFAULT_SOURCE
from app.shared.models.base import SoftDeleteMixin, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.modules.daily_logs.models import DailyLog
    from app.modules.imports.models import ImportRun
    from app.modules.notes.models import Note


class Category(UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "categories"

    owner_id: Mapped[UUID] = mapped_column(Uuid, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    normalized_name: Mapped[str] = mapped_column(String(120), nullable=False)

    tasks: Mapped[list[Task]] = relationship("Task", back_populates="category")


Index(
    "ix_categories_owner_normalized_name_active",
    Category.owner_id,
    Category.normalized_name,
    unique=True,
    sqlite_where=Category.deleted_at.is_(None),
    postgresql_where=Category.deleted_at.is_(None),
)


class Task(UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "tasks"
    __table_args__ = (
        CheckConstraint("time_spent_minutes > 0", name="ck_tasks_time_spent_positive"),
        Index("ix_tasks_owner_daily_log", "owner_id", "daily_log_id"),
        Index("ix_tasks_import_dedup", "owner_id", "normalized_title", "time_spent_minutes"),
    )

    owner_id: Mapped[UUID] = mapped_column(Uuid, nullable=False, index=True)
    daily_log_id: Mapped[UUID] = mapped_column(ForeignKey("daily_logs.id"), nullable=False, index=True)
    category_id: Mapped[UUID] = mapped_column(ForeignKey("categories.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    normalized_title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    time_spent_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    tags: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    source: Mapped[str] = mapped_column(String(32), nullable=False, default=str(DEFAULT_SOURCE))
    import_run_id: Mapped[UUID | None] = mapped_column(ForeignKey("import_runs.id"), nullable=True, index=True)

    daily_log: Mapped[DailyLog] = relationship("DailyLog", back_populates="tasks")
    category: Mapped[Category] = relationship("Category", back_populates="tasks")
    note: Mapped[Note | None] = relationship("Note", back_populates="task", uselist=False)
    import_run: Mapped[ImportRun | None] = relationship("ImportRun", back_populates="tasks")
