from datetime import UTC, date, datetime, timedelta
from uuid import UUID

from app.modules.ai_insights.constants import AI_INSIGHT_TARGET_PERIODS, AIInsightTargetPeriod
from app.modules.ai_insights.exceptions import (
    InvalidAIInsightStatusTransitionError,
    InvalidAIInsightTargetPeriodError,
)
from app.modules.ai_insights.models import AIInsightRun, AIInsightRunSource
from app.modules.ai_insights.repositories.ai_insight_run_repository import AIInsightRunRepository
from app.shared.enums.run_status import RunStatus, VALID_RUN_TRANSITIONS


class AIInsightRunService:
    def __init__(self, repository: AIInsightRunRepository) -> None:
        self.repository = repository

    async def create_ai_insight_run(
        self,
        owner_id: UUID,
        target_period_type: str,
        period_start: date,
        period_end: date,
        source_daily_log_ids: list[UUID],
    ) -> AIInsightRun:
        self._validate_target_period(target_period_type, period_start, period_end)
        ai_run = await self.repository.add(
            AIInsightRun(
                owner_id=owner_id,
                target_period_type=target_period_type,
                period_start=period_start,
                period_end=period_end,
                status=RunStatus.PENDING.value,
                source_summary={"source_daily_log_count": len(source_daily_log_ids)},
            )
        )
        for daily_log_id in source_daily_log_ids:
            source = AIInsightRunSource(
                owner_id=owner_id,
                ai_insight_run_id=ai_run.id,
                daily_log_id=daily_log_id,
                created_at=datetime.now(UTC),
            )
            source.ai_insight_run = ai_run
            await self.repository.add_source(source)
        loaded = await self.repository.get(ai_run.id)
        if loaded is None:
            raise InvalidAIInsightStatusTransitionError("created AI insight run could not be loaded")
        return loaded

    async def mark_ai_run_processing(self, ai_run_id: UUID) -> AIInsightRun:
        ai_run = await self._get_required(ai_run_id)
        self._ensure_transition(ai_run.status, RunStatus.PROCESSING.value)
        ai_run.status = RunStatus.PROCESSING.value
        ai_run.started_at = datetime.now(UTC)
        return ai_run

    async def complete_ai_run(
        self,
        ai_run_id: UUID,
        status: str,
        output_summary: dict[str, object] | None = None,
        failure_reason: str | None = None,
    ) -> AIInsightRun:
        ai_run = await self._get_required(ai_run_id)
        self._ensure_transition(ai_run.status, status)
        if status == RunStatus.FAILED.value and not (failure_reason or "").strip():
            raise InvalidAIInsightStatusTransitionError("failed AI runs require failure_reason")
        ai_run.status = status
        ai_run.output_summary = output_summary
        ai_run.failure_reason = failure_reason
        ai_run.completed_at = datetime.now(UTC)
        return ai_run

    async def create_rerun(self, ai_run_id: UUID) -> AIInsightRun:
        previous = await self._get_required(ai_run_id)
        return await self.create_ai_insight_run(
            owner_id=previous.owner_id,
            target_period_type=previous.target_period_type,
            period_start=previous.period_start,
            period_end=previous.period_end,
            source_daily_log_ids=[source.daily_log_id for source in previous.sources],
        )

    async def _get_required(self, ai_run_id: UUID) -> AIInsightRun:
        ai_run = await self.repository.get(ai_run_id)
        if ai_run is None:
            raise InvalidAIInsightStatusTransitionError("AI insight run not found")
        return ai_run

    @staticmethod
    def _validate_target_period(target_period_type: str, period_start: date, period_end: date) -> None:
        if target_period_type not in AI_INSIGHT_TARGET_PERIODS:
            raise InvalidAIInsightTargetPeriodError("target period type must be daily or weekly")
        if target_period_type == AIInsightTargetPeriod.DAILY.value and period_start != period_end:
            raise InvalidAIInsightTargetPeriodError("daily AI runs must start and end on the same date")
        if target_period_type == AIInsightTargetPeriod.WEEKLY.value and period_end - period_start != timedelta(days=6):
            raise InvalidAIInsightTargetPeriodError("weekly AI runs must cover exactly seven calendar days")

    @staticmethod
    def _ensure_transition(current_status: str, next_status: str) -> None:
        allowed = VALID_RUN_TRANSITIONS.get(RunStatus(current_status), set())
        if RunStatus(next_status) not in allowed:
            raise InvalidAIInsightStatusTransitionError(f"invalid status transition: {current_status} -> {next_status}")
