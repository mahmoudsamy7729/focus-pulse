from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Boolean, CheckConstraint, Date, DateTime, ForeignKey, Index, Integer, JSON, String, Text
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
        Index("ix_ai_insight_runs_owner_status_created", "owner_id", "status", "created_at"),
        Index("ix_ai_insight_runs_owner_period_idempotency", "owner_id", "target_period_type", "period_start", "period_end", "idempotency_key"),
        CheckConstraint("retry_count >= 0", name="ck_ai_insight_runs_retry_non_negative"),
        CheckConstraint("max_attempts >= 1", name="ck_ai_insight_runs_max_attempts_positive"),
    )

    owner_id: Mapped[UUID] = mapped_column(Uuid, nullable=False, index=True)
    target_period_type: Mapped[str] = mapped_column(String(32), nullable=False)
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default=RunStatus.PENDING.value, index=True)
    source_summary: Mapped[dict[str, object]] = mapped_column(JSON, nullable=False, default=dict)
    output_summary: Mapped[dict[str, object] | None] = mapped_column(JSON, nullable=True)
    failure_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    instruction_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    instruction_version: Mapped[str | None] = mapped_column(String(64), nullable=True)
    output_outcome: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    retry_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    max_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    idempotency_key: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    request_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    last_failure_stage: Mapped[str | None] = mapped_column(String(64), nullable=True)
    failure_details: Mapped[list[dict[str, object]]] = mapped_column(JSON, nullable=False, default=list)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    sources: Mapped[list[AIInsightRunSource]] = relationship(
        "AIInsightRunSource",
        back_populates="ai_insight_run",
        cascade="all, delete-orphan",
    )
    insight_results: Mapped[list[AIInsightResult]] = relationship("AIInsightResult", back_populates="source_ai_insight_run")


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


class AIInsightResult(UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "ai_insight_results"
    __table_args__ = (
        Index("ix_ai_insight_results_owner_period_current", "owner_id", "period_granularity", "period_start", "period_end", "is_current"),
        Index("ix_ai_insight_results_owner_generated", "owner_id", "generated_at"),
        Index("ix_ai_insight_results_source_run", "source_ai_insight_run_id"),
        Index(
            "ix_ai_insight_results_default_reuse",
            "owner_id",
            "period_granularity",
            "period_start",
            "period_end",
            "source_ai_insight_run_id",
            "status",
        ),
        Index("ix_ai_insight_results_idempotency", "owner_id", "idempotency_key"),
        CheckConstraint("period_end >= period_start", name="ck_ai_insight_results_period_order"),
    )

    owner_id: Mapped[UUID] = mapped_column(Uuid, nullable=False, index=True)
    period_granularity: Mapped[str] = mapped_column(String(32), nullable=False)
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    source_ai_insight_run_id: Mapped[UUID] = mapped_column(ForeignKey("ai_insight_runs.id"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    is_current: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    generation_reason: Mapped[str] = mapped_column(String(32), nullable=False)
    idempotency_key: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    request_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    source_snapshot: Mapped[dict[str, object]] = mapped_column(JSON, nullable=False, default=dict)
    productivity_score: Mapped[dict[str, object]] = mapped_column(JSON, nullable=False, default=dict)
    consistency_score: Mapped[dict[str, object] | None] = mapped_column(JSON, nullable=True)
    best_day_finding: Mapped[dict[str, object] | None] = mapped_column(JSON, nullable=True)
    worst_day_finding: Mapped[dict[str, object] | None] = mapped_column(JSON, nullable=True)
    recommendations: Mapped[list[dict[str, object]]] = mapped_column(JSON, nullable=False, default=list)
    evidence: Mapped[list[dict[str, object]]] = mapped_column(JSON, nullable=False, default=list)
    validation_outcome: Mapped[dict[str, object]] = mapped_column(JSON, nullable=False, default=dict)
    failure_code: Mapped[str | None] = mapped_column(String(120), nullable=True)
    failure_details: Mapped[dict[str, object] | None] = mapped_column(JSON, nullable=True)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    source_ai_insight_run: Mapped[AIInsightRun] = relationship("AIInsightRun", back_populates="insight_results")
    sources: Mapped[list[AIInsightResultSource]] = relationship(
        "AIInsightResultSource",
        back_populates="ai_insight_result",
        cascade="all, delete-orphan",
    )


class AIInsightResultSource(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "ai_insight_result_sources"
    __table_args__ = (
        Index("ix_ai_insight_result_sources_unique_source", "ai_insight_result_id", "daily_log_id", unique=True),
        Index("ix_ai_insight_result_sources_owner_result", "owner_id", "ai_insight_result_id"),
    )

    owner_id: Mapped[UUID] = mapped_column(Uuid, nullable=False, index=True)
    ai_insight_result_id: Mapped[UUID] = mapped_column(ForeignKey("ai_insight_results.id"), nullable=False, index=True)
    daily_log_id: Mapped[UUID] = mapped_column(ForeignKey("daily_logs.id"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    ai_insight_result: Mapped[AIInsightResult] = relationship("AIInsightResult", back_populates="sources")
    daily_log: Mapped[DailyLog] = relationship("DailyLog")
