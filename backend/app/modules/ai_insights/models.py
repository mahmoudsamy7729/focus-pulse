from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Date, DateTime, ForeignKey, Index, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from app.core.database import Base
from app.shared.enums.run_status import RunStatus
from app.shared.models.base import SoftDeleteMixin, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.modules.daily_logs.models import DailyLog


class AIInsightRun(UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "ai_insight_runs"
    __table_args__ = (
        Index("ix_ai_insight_runs_owner_period", "owner_id", "target_period_type", "period_start", "period_end"),
    )

    owner_id: Mapped[UUID] = mapped_column(Uuid, nullable=False, index=True)
    target_period_type: Mapped[str] = mapped_column(String(32), nullable=False)
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default=RunStatus.PENDING.value, index=True)
    source_summary: Mapped[dict[str, object]] = mapped_column(JSON, nullable=False, default=dict)
    output_summary: Mapped[dict[str, object] | None] = mapped_column(JSON, nullable=True)
    failure_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    sources: Mapped[list[AIInsightRunSource]] = relationship(
        "AIInsightRunSource",
        back_populates="ai_insight_run",
        cascade="all, delete-orphan",
    )


class AIInsightRunSource(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "ai_insight_run_sources"
    __table_args__ = (
        Index(
            "ix_ai_insight_run_sources_unique_source",
            "ai_insight_run_id",
            "daily_log_id",
            unique=True,
        ),
    )

    owner_id: Mapped[UUID] = mapped_column(Uuid, nullable=False, index=True)
    ai_insight_run_id: Mapped[UUID] = mapped_column(ForeignKey("ai_insight_runs.id"), nullable=False, index=True)
    daily_log_id: Mapped[UUID] = mapped_column(ForeignKey("daily_logs.id"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    ai_insight_run: Mapped[AIInsightRun] = relationship("AIInsightRun", back_populates="sources")
    daily_log: Mapped[DailyLog] = relationship("DailyLog", back_populates="ai_sources")
