from __future__ import annotations

import logging
from datetime import UTC, datetime
from uuid import UUID

from app.core.config import get_settings
from app.modules.ai_insights.constants import AIInsightFailureStage, AIInsightOutputOutcome
from app.modules.ai_insights.exceptions import AIOutputValidationError, AIProviderFailureError
from app.modules.ai_insights.providers.base import AIAnalysisProvider, AIProviderRequest
from app.modules.ai_insights.repositories.ai_insight_run_repository import AIInsightRunRepository
from app.modules.ai_insights.schemas import CombinedAnalysisOutput, RunFailureDetail
from app.modules.ai_insights.services.ai_input_service import AIInputService
from app.modules.ai_insights.services.ai_instruction_service import AIInstructionService
from app.modules.ai_insights.services.ai_output_validator import AIOutputValidator
from app.modules.ai_insights.services.ai_insight_run_service import AIInsightRunService
from app.shared.enums.run_status import RunStatus

logger = logging.getLogger(__name__)


class AIAnalysisService:
    def __init__(
        self,
        run_repository: AIInsightRunRepository,
        input_service: AIInputService,
        instruction_service: AIInstructionService,
        provider: AIAnalysisProvider,
        output_validator: AIOutputValidator,
    ) -> None:
        self.run_repository = run_repository
        self.run_service = AIInsightRunService(run_repository)
        self.input_service = input_service
        self.instruction_service = instruction_service
        self.provider = provider
        self.output_validator = output_validator
        self.settings = get_settings()

    async def process_analysis_run(self, ai_insight_run_id: UUID) -> dict[str, object]:
        ai_run = await self.run_repository.get(ai_insight_run_id)
        if ai_run is None:
            raise AIProviderFailureError("AI insight run not found.", transient=False)

        logger.info("ai_analysis_started", extra={"ai_insight_run_id": str(ai_run.id), "request_id": ai_run.request_id})
        await self.run_service.mark_ai_run_processing(ai_run.id)
        instruction = self.instruction_service.get_instruction(ai_run.target_period_type)
        ai_run.instruction_name = instruction.instruction_name
        ai_run.instruction_version = instruction.instruction_version

        try:
            prepared = await self.input_service.prepare_input(
                ai_run.owner_id,
                ai_run.target_period_type,
                ai_run.period_start,
                instruction.instruction_name,
                instruction.instruction_version,
            )
            ai_run.source_summary = prepared.source_summary.model_dump(mode="json")
            await self.run_repository.replace_sources(ai_run, prepared.source_daily_log_ids)

            if prepared.source_summary.task_count == 0:
                output = CombinedAnalysisOutput(
                    output_outcome=AIInsightOutputOutcome.NO_DATA.value,
                    generated_at=datetime.now(UTC),
                    summary=None,
                    detected_patterns=[],
                    behavior_insights=[],
                    supporting_evidence=[],
                    limitations=["No saved tracking records were available for this period."],
                )
                await self.run_service.complete_ai_run(
                    ai_run.id,
                    RunStatus.COMPLETED.value,
                    output.model_dump(mode="json"),
                    output_outcome=AIInsightOutputOutcome.NO_DATA.value,
                )
                return {"ai_insight_run_id": str(ai_run.id), "status": RunStatus.COMPLETED.value}

            attempt = 1
            while attempt <= ai_run.max_attempts:
                try:
                    response = await self.provider.generate_analysis(
                        AIProviderRequest(
                            input=prepared.provider_input,
                            prompt=instruction.prompt,
                            model=self.settings.ai.model,
                            timeout_seconds=self.settings.ai.request_timeout_seconds,
                        )
                    )
                    validated = self.output_validator.validate_output(response.output, prepared.provider_input)
                    ai_run.retry_count = max(ai_run.retry_count, attempt - 1)
                    await self.run_service.complete_ai_run(
                        ai_run.id,
                        RunStatus.COMPLETED.value,
                        validated.model_dump(mode="json"),
                        output_outcome=validated.output_outcome,
                    )
                    logger.info(
                        "ai_analysis_completed",
                        extra={"ai_insight_run_id": str(ai_run.id), "retry_count": ai_run.retry_count},
                    )
                    return {"ai_insight_run_id": str(ai_run.id), "status": RunStatus.COMPLETED.value}
                except AIOutputValidationError as exc:
                    await self._record_failure(ai_run.id, AIInsightFailureStage.OUTPUT_VALIDATION.value, str(exc), attempt, False)
                    raise
                except AIProviderFailureError as exc:
                    await self._record_failure(ai_run.id, AIInsightFailureStage.PROVIDER_CALL.value, str(exc), attempt, exc.transient)
                    if not exc.transient or attempt >= ai_run.max_attempts:
                        await self.run_service.fail_ai_run(ai_run.id, str(exc))
                        return {"ai_insight_run_id": str(ai_run.id), "status": RunStatus.FAILED.value}
                    attempt += 1
                    continue
        except Exception as exc:
            if not isinstance(exc, (AIOutputValidationError, AIProviderFailureError)):
                await self._record_failure(ai_run.id, AIInsightFailureStage.WORKER_EXECUTION.value, str(exc), 1, False)
            await self.run_service.fail_ai_run(ai_run.id, str(exc))
            return {"ai_insight_run_id": str(ai_run.id), "status": RunStatus.FAILED.value}

        return {"ai_insight_run_id": str(ai_run.id), "status": ai_run.status}

    async def _record_failure(self, ai_run_id: UUID, stage: str, reason: str, attempt: int, transient: bool) -> None:
        detail = RunFailureDetail(
            stage=stage,
            reason=reason,
            attempt_number=attempt,
            transient=transient,
            occurred_at=datetime.now(UTC),
        )
        await self.run_service.record_failure_detail(ai_run_id, detail.model_dump(mode="json"))
