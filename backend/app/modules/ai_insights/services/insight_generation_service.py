from __future__ import annotations

import logging
from datetime import UTC, date, datetime
from uuid import UUID

from app.modules.ai_insights.constants import InsightGenerationReason, InsightResultStatus
from app.modules.ai_insights.exceptions import InsightGenerationConflictError, InsightValidationFailureError
from app.modules.ai_insights.models import AIInsightResult
from app.modules.ai_insights.repositories.ai_insight_result_repository import AIInsightResultRepository
from app.modules.ai_insights.schemas import InsightResultMutationResponse, InsightResultRead
from app.modules.ai_insights.services.consistency_scoring_service import ConsistencyScoringService
from app.modules.ai_insights.services.day_ranking_service import DayRankingService
from app.modules.ai_insights.services.insight_source_service import InsightSourceService
from app.modules.ai_insights.services.insight_validation_service import InsightValidationService
from app.modules.ai_insights.services.productivity_scoring_service import ProductivityScoringService
from app.modules.ai_insights.services.recommendation_service import RecommendationService

logger = logging.getLogger(__name__)


class InsightGenerationService:
    def __init__(
        self,
        result_repository: AIInsightResultRepository,
        source_service: InsightSourceService,
        productivity_scoring_service: ProductivityScoringService,
        consistency_scoring_service: ConsistencyScoringService,
        day_ranking_service: DayRankingService,
        recommendation_service: RecommendationService,
        validation_service: InsightValidationService,
    ) -> None:
        self.result_repository = result_repository
        self.source_service = source_service
        self.productivity_scoring_service = productivity_scoring_service
        self.consistency_scoring_service = consistency_scoring_service
        self.day_ranking_service = day_ranking_service
        self.recommendation_service = recommendation_service
        self.validation_service = validation_service

    async def generate(
        self,
        owner_id: UUID,
        period_granularity: str,
        period_start: date,
        period_end: date,
        *,
        source_ai_insight_run_id: UUID | None = None,
        generation_reason: str = InsightGenerationReason.DEFAULT_GENERATE.value,
        idempotency_key: str | None = None,
        request_id: str | None = None,
    ) -> InsightResultMutationResponse:
        if idempotency_key:
            existing_key = await self.result_repository.find_by_idempotency_key(owner_id, idempotency_key)
            if existing_key is not None:
                if (
                    existing_key.period_granularity != period_granularity
                    or existing_key.period_start != period_start
                    or existing_key.period_end != period_end
                ):
                    raise InsightGenerationConflictError("Idempotency key was already used for a different insight period.")
                return InsightResultMutationResponse(result=self._read(existing_key), reused_existing=True)

        source = await self.source_service.resolve_source_analysis(
            owner_id,
            period_granularity,
            period_start,
            period_end,
            source_ai_insight_run_id,
        )
        if generation_reason == InsightGenerationReason.DEFAULT_GENERATE.value:
            existing = await self.result_repository.find_default_reuse(
                owner_id,
                period_granularity,
                period_start,
                period_end,
                source.id,
            )
            if existing is not None:
                logger.info(
                    "ai_insight_result_reused",
                    extra={
                        "owner_id": str(owner_id),
                        "ai_insight_result_id": str(existing.id),
                        "source_ai_insight_run_id": str(source.id),
                        "period_granularity": period_granularity,
                        "request_id": request_id,
                    },
                )
                return InsightResultMutationResponse(result=self._read(existing), reused_existing=True)

        snapshot, evidence = self.source_service.build_snapshot_and_evidence(source)
        productivity_score = self.productivity_scoring_service.score(snapshot, evidence)
        consistency_score = self.consistency_scoring_service.score(snapshot, evidence)
        best_day_finding, worst_day_finding = self.day_ranking_service.rank(snapshot)
        recommendations = self.recommendation_service.recommend(
            snapshot,
            productivity_score,
            consistency_score,
            best_day_finding,
            worst_day_finding,
        )
        validation_outcome = self.validation_service.validate(
            snapshot,
            productivity_score,
            consistency_score,
            best_day_finding,
            worst_day_finding,
            recommendations,
            evidence,
        )
        now = datetime.now(UTC)
        result = AIInsightResult(
            owner_id=owner_id,
            period_granularity=period_granularity,
            period_start=period_start,
            period_end=period_end,
            source_ai_insight_run_id=source.id,
            status=InsightResultStatus.COMPLETED.value if validation_outcome.passed else InsightResultStatus.FAILED.value,
            is_current=False,
            generation_reason=generation_reason,
            idempotency_key=idempotency_key,
            request_id=request_id,
            source_snapshot=snapshot.model_dump(mode="json"),
            productivity_score=productivity_score.model_dump(mode="json"),
            consistency_score=consistency_score.model_dump(mode="json") if consistency_score else None,
            best_day_finding=best_day_finding.model_dump(mode="json") if best_day_finding else None,
            worst_day_finding=worst_day_finding.model_dump(mode="json") if worst_day_finding else None,
            recommendations=[item.model_dump(mode="json") for item in recommendations],
            evidence=[item.model_dump(mode="json") for item in evidence],
            validation_outcome=validation_outcome.model_dump(mode="json"),
            failure_code=None if validation_outcome.passed else "INSIGHT_VALIDATION_FAILED",
            failure_details=None if validation_outcome.passed else {"failure_codes": validation_outcome.failure_codes},
            generated_at=now,
        )
        await self.result_repository.add(result)
        await self.result_repository.add_sources(result, snapshot.source_daily_log_ids)
        if validation_outcome.passed:
            await self.result_repository.clear_current(owner_id, period_granularity, period_start, period_end)
            result.is_current = True
        logger.info(
            "ai_insight_result_generated",
            extra={
                "owner_id": str(owner_id),
                "ai_insight_result_id": str(result.id),
                "source_ai_insight_run_id": str(source.id),
                "period_granularity": period_granularity,
                "validation_passed": validation_outcome.passed,
                "generation_reason": generation_reason,
                "request_id": request_id,
            },
        )
        if not validation_outcome.passed:
            raise InsightValidationFailureError("Generated insight result failed validation.")
        return InsightResultMutationResponse(result=self._read(result), reused_existing=False)

    @staticmethod
    def _read(result: AIInsightResult) -> InsightResultRead:
        return InsightResultRead.model_validate(result)
