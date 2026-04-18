from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Date, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from app.core.database import Base
from app.shared.enums.source import DEFAULT_SOURCE
from app.shared.models.base import SoftDeleteMixin, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.modules.ai_insights.models import AIInsightRunSource
    from app.modules.tasks.models import Task


class DailyLog(UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "daily_logs"

    owner_id: Mapped[UUID] = mapped_column(Uuid, nullable=False, index=True)
    log_date: Mapped[date] = mapped_column(Date, nullable=False)
    source: Mapped[str] = mapped_column(String(32), nullable=False, default=str(DEFAULT_SOURCE))

    tasks: Mapped[list[Task]] = relationship("Task", back_populates="daily_log")
    ai_sources: Mapped[list[AIInsightRunSource]] = relationship(
        "AIInsightRunSource",
        back_populates="daily_log",
    )


Index(
    "ix_daily_logs_owner_log_date_active",
    DailyLog.owner_id,
    DailyLog.log_date,
    unique=True,
    sqlite_where=DailyLog.deleted_at.is_(None),
    postgresql_where=DailyLog.deleted_at.is_(None),
)

# Register the reverse relationship target when DailyLog is imported at runtime.
from app.modules.ai_insights.models import AIInsightRunSource  # noqa: E402,F401
