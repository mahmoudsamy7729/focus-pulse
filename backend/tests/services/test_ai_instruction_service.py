import pytest

from app.modules.ai_insights.exceptions import InvalidAIInsightTargetPeriodError
from app.modules.ai_insights.providers.base import AIProviderRequest, DeterministicAIAnalysisProvider
from app.modules.ai_insights.schemas import AnalysisInputSummary, StructuredAIInput
from app.modules.ai_insights.services.ai_instruction_service import AIInstructionService


def test_instruction_service_selects_stable_daily_and_weekly_versions() -> None:
    service = AIInstructionService()

    daily = service.get_instruction("daily")
    weekly = service.get_instruction("weekly")

    assert daily.instruction_name == "daily_combined_analysis"
    assert weekly.instruction_name == "weekly_combined_analysis"
    assert daily.instruction_version == weekly.instruction_version
    assert "note text" in daily.prompt


def test_instruction_service_rejects_invalid_period() -> None:
    with pytest.raises(InvalidAIInsightTargetPeriodError):
        AIInstructionService().get_instruction("monthly")


@pytest.mark.asyncio
async def test_deterministic_provider_requires_task_input() -> None:
    instruction = AIInstructionService().get_instruction("daily")
    provider_input = StructuredAIInput(
        period_granularity="daily",
        period_start="2026-04-15",
        period_end="2026-04-15",
        tasks=[],
        aggregates=AnalysisInputSummary(),
        instruction_name=instruction.instruction_name,
        instruction_version=instruction.instruction_version,
    )

    with pytest.raises(Exception):
        await DeterministicAIAnalysisProvider().generate_analysis(
            AIProviderRequest(input=provider_input, prompt=instruction.prompt, model="test", timeout_seconds=1)
        )
