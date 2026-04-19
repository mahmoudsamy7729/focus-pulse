from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from typing import Callable
from uuid import UUID

from app.modules.ai_insights.constants import (
    AI_INSIGHT_DEFAULT_LIMIT,
    AI_INSIGHT_DEFAULT_PAGE,
    AI_INSIGHT_MAX_ATTEMPTS,
    AI_INSIGHT_MAX_LIMIT,
    AI_INSIGHT_TARGET_PERIODS,
    AIInsightOutputOutcome,
    AIInsightTargetPeriod,
)
from app.modules.ai_insights.exceptions import (
    AIInsightConflictError,
    AIInsightNotFoundError,
    InvalidAIInsightStatusTransitionError,
    InvalidAIInsightTargetPeriodError,
)
from app.modules.ai_insights.models import AIInsightRun, AIInsightRunSource
from app.modules.ai_insights.repositories.ai_insight_run_repository import AIInsightRunRepository
from app.modules.ai_insights.schemas import (
    AIInsightRunAccepted,
    AIInsightRunDetail,
    AIInsightRunPage,
    AnalysisInputSummary,
    CurrentAIInsightRun,
)
from app.shared.enums.run_status import RunStatus, VALID_RUN_TRANSITIONS

EnqueueAnalysisRun = Callable[[UUID, UUID], object]


class AIInsightRunService:
    def __init__(
        self,
        repository: AIInsightRunRepository,
        *,
        enqueue_analysis_run: EnqueueAnalysisRun | None = None,
    ) -> None:
        self.repository = repository
        self.enqueue_analysis_run = enqueue_analysis_run

    async def request_analysis_run(
        self,
        owner_id: UUID,
        period_granularity: str,
        anchor_date: date,
        *,
        idempotency_key: str | None = None,
        request_id: str | None = None,
    ) -> AIInsightRunAccepted:
        period_start, period_end = self.resolve_period(period_granularity, anchor_date)
        if idempotency_key:
            existing = await self.repository.find_by_idempotency_key(
                owner_id, period_granularity, period_start, period_end, idempotency_key
            )
            if existing is not None:
                return self._accepted(existing, reused_existing=True)

        in_flight = await self.repository.find_in_flight(owner_id, period_granularity, period_start, period_end)
        if in_flight is not None:
            raise AIInsightConflictError("An AI insight run is already pending or processing for this period.")

        ai_run = await self.create_ai_insight_run(
            owner_id,
            period_granularity,
            period_start,
            period_end,
            [],
            idempotency_key=idempotency_key,
            request_id=request_id,
        )
        self._enqueue(ai_run)
        return self._accepted(ai_run)

    async def create_ai_insight_run(
        self,
        owner_id: UUID,
        target_period_type: str,
        period_start: date,
        period_end: date,
        source_daily_log_ids: list[UUID],
        *,
        idempotency_key: str | None = None,
        request_id: str | None = None,
        source_summary: dict[str, object] | None = None,
    ) -> AIInsightRun:
        self._validate_target_period(target_period_type, period_start, period_end)
        ai_run = await self.repository.add(
            AIInsightRun(
                owner_id=owner_id,
                target_period_type=target_period_type,
                period_start=period_start,
                period_end=period_end,
                status=RunStatus.PENDING.value,
                source_summary=source_summary or AnalysisInputSummary(
                    source_daily_log_ids=source_daily_log_ids,
                    daily_log_count=len(source_daily_log_ids),
                ).model_dump(mode="json"),
                retry_count=0,
                max_attempts=AI_INSIGHT_MAX_ATTEMPTS,
                idempotency_key=idempotency_key,
                request_id=request_id,
                failure_details=[],
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
        if ai_run.status != RunStatus.PROCESSING.value:
            self._ensure_transition(ai_run.status, RunStatus.PROCESSING.value)
        ai_run.status = RunStatus.PROCESSING.value
        ai_run.started_at = ai_run.started_at or datetime.now(UTC)
        return ai_run

    async def complete_ai_run(
        self,
        ai_run_id: UUID,
        status: str,
        output_summary: dict[str, object] | None = None,
        failure_reason: str | None = None,
        *,
        output_outcome: str | None = None,
    ) -> AIInsightRun:
        ai_run = await self._get_required(ai_run_id)
        self._ensure_transition(ai_run.status, status)
        if status == RunStatus.FAILED.value and not (failure_reason or "").strip():
            raise InvalidAIInsightStatusTransitionError("failed AI runs require failure_reason")
        ai_run.status = status
        ai_run.output_summary = output_summary
        ai_run.output_outcome = output_outcome or (output_summary or {}).get("output_outcome")  # type: ignore[assignment]
        ai_run.failure_reason = failure_reason
        ai_run.completed_at = datetime.now(UTC)
        return ai_run

    async def fail_ai_run(self, ai_run_id: UUID, failure_reason: str) -> AIInsightRun:
        ai_run = await self._get_required(ai_run_id)
        if ai_run.status != RunStatus.FAILED.value:
            ai_run.status = RunStatus.FAILED.value
        ai_run.failure_reason = failure_reason
        ai_run.completed_at = datetime.now(UTC)
        return ai_run

    async def record_failure_detail(self, ai_run_id: UUID, detail: dict[str, object]) -> AIInsightRun:
        ai_run = await self._get_required(ai_run_id)
        details = list(ai_run.failure_details or [])
        details.append(detail)
        ai_run.failure_details = details
        ai_run.last_failure_stage = str(detail.get("stage") or "")
        attempt_number = int(detail.get("attempt_number") or 1)
        ai_run.retry_count = max(ai_run.retry_count, max(0, attempt_number - 1))
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

    async def request_rerun(
        self,
        owner_id: UUID,
        ai_run_id: UUID,
        *,
        idempotency_key: str | None = None,
    ) -> AIInsightRunAccepted:
        previous = await self.repository.get_for_owner(owner_id, ai_run_id)
        if previous is None:
            raise AIInsightNotFoundError("AI insight run was not found for the current owner.")
        in_flight = await self.repository.find_in_flight(
            owner_id,
            previous.target_period_type,
            previous.period_start,
            previous.period_end,
        )
        if in_flight is not None:
            raise AIInsightConflictError("An AI insight run is already pending or processing for this period.")
        rerun = await self.create_ai_insight_run(
            owner_id,
            previous.target_period_type,
            previous.period_start,
            previous.period_end,
            [source.daily_log_id for source in previous.sources],
            idempotency_key=idempotency_key,
        )
        self._enqueue(rerun)
        return self._accepted(rerun)

    async def get_run_detail(self, owner_id: UUID, ai_run_id: UUID) -> AIInsightRunDetail:
        ai_run = await self.repository.get_for_owner(owner_id, ai_run_id)
        if ai_run is None:
            raise AIInsightNotFoundError("AI insight run was not found for the current owner.")
        return self._detail(ai_run)

    async def list_history(
        self,
        owner_id: UUID,
        *,
        page: int = AI_INSIGHT_DEFAULT_PAGE,
        limit: int = AI_INSIGHT_DEFAULT_LIMIT,
        period_granularity: str | None = None,
        status: str | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> AIInsightRunPage:
        self._validate_pagination(page, limit)
        if period_granularity is not None and period_granularity not in AI_INSIGHT_TARGET_PERIODS:
            raise InvalidAIInsightTargetPeriodError("period_granularity must be daily or weekly")
        items, total = await self.repository.list_for_owner(
            owner_id,
            page=page,
            limit=limit,
            target_period_type=period_granularity,
            status=status,
            start_date=start_date,
            end_date=end_date,
        )
        return AIInsightRunPage(page=page, limit=limit, total=total, items=[self._detail(item) for item in items])

    async def get_current_result(self, owner_id: UUID, period_granularity: str, anchor_date: date) -> CurrentAIInsightRun:
        period_start, period_end = self.resolve_period(period_granularity, anchor_date)
        current = await self.repository.find_current_result(owner_id, period_granularity, period_start, period_end)
        return CurrentAIInsightRun(
            period_granularity=period_granularity,
            period_start=period_start,
            period_end=period_end,
            current_run=self._detail(current) if current is not None else None,
        )

    async def _get_required(self, ai_run_id: UUID) -> AIInsightRun:
        ai_run = await self.repository.get(ai_run_id)
        if ai_run is None:
            raise InvalidAIInsightStatusTransitionError("AI insight run not found")
        return ai_run

    @staticmethod
    def resolve_period(period_granularity: str, anchor_date: date) -> tuple[date, date]:
        if period_granularity == AIInsightTargetPeriod.DAILY.value:
            return anchor_date, anchor_date
        if period_granularity == AIInsightTargetPeriod.WEEKLY.value:
            start = anchor_date - timedelta(days=anchor_date.weekday())
            return start, start + timedelta(days=6)
        raise InvalidAIInsightTargetPeriodError("period_granularity must be daily or weekly")

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
        if current_status == next_status:
            return
        allowed = VALID_RUN_TRANSITIONS.get(RunStatus(current_status), set())
        if RunStatus(next_status) not in allowed:
            raise InvalidAIInsightStatusTransitionError(f"invalid status transition: {current_status} -> {next_status}")

    @staticmethod
    def _validate_pagination(page: int, limit: int) -> None:
        if page < 1:
            raise InvalidAIInsightTargetPeriodError("page must be greater than or equal to 1")
        if limit < 1 or limit > AI_INSIGHT_MAX_LIMIT:
            raise InvalidAIInsightTargetPeriodError(f"limit must be between 1 and {AI_INSIGHT_MAX_LIMIT}")

    def _enqueue(self, ai_run: AIInsightRun) -> None:
        if self.enqueue_analysis_run is not None:
            self.enqueue_analysis_run(ai_run.id, ai_run.owner_id)

    @staticmethod
    def _accepted(ai_run: AIInsightRun, *, reused_existing: bool = False) -> AIInsightRunAccepted:
        return AIInsightRunAccepted(
            ai_insight_run_id=ai_run.id,
            status=ai_run.status,
            period_granularity=ai_run.target_period_type,
            period_start=ai_run.period_start,
            period_end=ai_run.period_end,
            reused_existing=reused_existing,
        )

    @staticmethod
    def _detail(ai_run: AIInsightRun) -> AIInsightRunDetail:
        output_summary = ai_run.output_summary
        if output_summary and output_summary.get("output_outcome") == AIInsightOutputOutcome.NO_DATA.value:
            output_summary = dict(output_summary)
        return AIInsightRunDetail(
            id=ai_run.id,
            status=ai_run.status,
            period_granularity=ai_run.target_period_type,
            period_start=ai_run.period_start,
            period_end=ai_run.period_end,
            instruction_name=ai_run.instruction_name,
            instruction_version=ai_run.instruction_version,
            output_outcome=ai_run.output_outcome,
            source_summary=ai_run.source_summary,
            output_summary=output_summary,
            failure_reason=ai_run.failure_reason,
            failure_details=ai_run.failure_details or [],
            retry_count=ai_run.retry_count,
            max_attempts=ai_run.max_attempts,
            started_at=ai_run.started_at,
            completed_at=ai_run.completed_at,
            created_at=ai_run.created_at,
        )
