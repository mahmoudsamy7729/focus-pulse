from __future__ import annotations

import logging
from datetime import date
from uuid import UUID

from app.modules.ai_insights.constants import (
    AI_INSIGHT_DEFAULT_LIMIT,
    AI_INSIGHT_DEFAULT_PAGE,
    AI_INSIGHT_MAX_LIMIT,
    AI_INSIGHT_TARGET_PERIODS,
    INSIGHT_RESULT_STATUSES,
    InsightGenerationReason,
)
from app.modules.ai_insights.exceptions import InsightResultNotFoundError, InvalidInsightPeriodError
from app.modules.ai_insights.repositories.ai_insight_result_repository import AIInsightResultRepository
from app.modules.ai_insights.schemas import CurrentInsightResult, InsightResultPage, InsightResultRead
from app.modules.ai_insights.services.ai_insight_run_service import AIInsightRunService
from app.modules.ai_insights.services.insight_generation_service import InsightGenerationService

logger = logging.getLogger(__name__)


class InsightResultService:
    def __init__(
        self,
        repository: AIInsightResultRepository,
        generation_service: InsightGenerationService,
    ) -> None:
        self.repository = repository
        self.generation_service = generation_service

    async def get_current(self, owner_id: UUID, period_granularity: str, anchor_date: date) -> CurrentInsightResult:
        period_start, period_end = self.resolve_period(period_granularity, anchor_date)
        current = await self.repository.find_current(owner_id, period_granularity, period_start, period_end)
        return CurrentInsightResult(
            period_granularity=period_granularity,  # type: ignore[arg-type]
            period_start=period_start,
            period_end=period_end,
            current_result=InsightResultRead.model_validate(current) if current else None,
        )

    async def get_detail(self, owner_id: UUID, result_id: UUID) -> InsightResultRead:
        result = await self.repository.get_for_owner(owner_id, result_id)
        if result is None:
            raise InsightResultNotFoundError("Insight result was not found for the current owner.")
        return InsightResultRead.model_validate(result)

    async def rerun(
        self,
        owner_id: UUID,
        result_id: UUID,
        *,
        idempotency_key: str | None = None,
        request_id: str | None = None,
    ):
        previous = await self.repository.get_for_owner(owner_id, result_id)
        if previous is None:
            raise InsightResultNotFoundError("Insight result was not found for the current owner.")
        logger.info(
            "ai_insight_result_rerun_requested",
            extra={"owner_id": str(owner_id), "ai_insight_result_id": str(result_id), "request_id": request_id},
        )
        return await self.generation_service.generate(
            owner_id,
            previous.period_granularity,
            previous.period_start,
            previous.period_end,
            source_ai_insight_run_id=previous.source_ai_insight_run_id,
            generation_reason=InsightGenerationReason.EXPLICIT_RERUN.value,
            idempotency_key=idempotency_key,
            request_id=request_id,
        )

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
    ) -> InsightResultPage:
        self._validate_pagination(page, limit)
        if period_granularity is not None and period_granularity not in AI_INSIGHT_TARGET_PERIODS:
            raise InvalidInsightPeriodError("period_granularity must be daily or weekly")
        if status is not None and status not in INSIGHT_RESULT_STATUSES:
            raise InvalidInsightPeriodError("status must be completed or failed")
        items, total = await self.repository.list_for_owner(
            owner_id,
            page=page,
            limit=limit,
            period_granularity=period_granularity,
            status=status,
            start_date=start_date,
            end_date=end_date,
        )
        return InsightResultPage(page=page, limit=limit, total=total, items=[InsightResultRead.model_validate(item) for item in items])

    @staticmethod
    def resolve_period(period_granularity: str, anchor_date: date) -> tuple[date, date]:
        try:
            return AIInsightRunService.resolve_period(period_granularity, anchor_date)
        except Exception as exc:
            raise InvalidInsightPeriodError(str(exc)) from exc

    @staticmethod
    def _validate_pagination(page: int, limit: int) -> None:
        if page < 1:
            raise InvalidInsightPeriodError("page must be greater than or equal to 1")
        if limit < 1 or limit > AI_INSIGHT_MAX_LIMIT:
            raise InvalidInsightPeriodError(f"limit must be between 1 and {AI_INSIGHT_MAX_LIMIT}")
