from __future__ import annotations

from datetime import UTC, datetime
from typing import Protocol

from pydantic import BaseModel

from app.modules.ai_insights.exceptions import AIProviderFailureError
from app.modules.ai_insights.schemas import CombinedAnalysisOutput, StructuredAIInput, SupportingEvidence, AnalysisObservation


class AIProviderRequest(BaseModel):
    input: StructuredAIInput
    prompt: str
    model: str
    timeout_seconds: float


class AIProviderResponse(BaseModel):
    output: dict[str, object]
    provider_name: str
    model: str


class AIAnalysisProvider(Protocol):
    async def generate_analysis(self, request: AIProviderRequest) -> AIProviderResponse:
        """Generate one combined AI analysis output."""


class DeterministicAIAnalysisProvider:
    """Deterministic provider used for local development and tests."""

    provider_name = "deterministic"

    async def generate_analysis(self, request: AIProviderRequest) -> AIProviderResponse:
        provider_input = request.input
        if not provider_input.tasks:
            raise AIProviderFailureError("deterministic provider received no tasks", transient=False)

        evidence: list[SupportingEvidence] = [
            SupportingEvidence(
                evidence_id="e_task_count",
                evidence_type="task_count",
                count=provider_input.aggregates.task_count,
            )
        ]
        for index, total in enumerate(provider_input.aggregates.category_totals[:3], start=1):
            evidence.append(
                SupportingEvidence(
                    evidence_id=f"e_category_{index}",
                    evidence_type="category_total",
                    label=total.label,
                    minutes=total.total_minutes,
                )
            )
        for index, total in enumerate(provider_input.aggregates.tag_totals[:3], start=1):
            evidence.append(
                SupportingEvidence(
                    evidence_id=f"e_tag_{index}",
                    evidence_type="tag_total",
                    label=total.label,
                    minutes=total.total_minutes,
                )
            )

        evidence_ids = [item.evidence_id for item in evidence]
        summary = (
            f"Tracked {provider_input.aggregates.total_minutes} minutes across "
            f"{provider_input.aggregates.task_count} tasks."
        )
        detected_patterns: list[AnalysisObservation] = []
        behavior_insights: list[AnalysisObservation] = []
        if provider_input.aggregates.category_totals:
            top_category = provider_input.aggregates.category_totals[0]
            detected_patterns.append(
                AnalysisObservation(
                    text=f"{top_category.label} accounted for {top_category.total_minutes} tracked minutes.",
                    evidence_ids=["e_category_1"],
                )
            )
        if provider_input.aggregates.tag_totals:
            top_tag = provider_input.aggregates.tag_totals[0]
            behavior_insights.append(
                AnalysisObservation(
                    text=f"Tasks tagged {top_tag.label} were a visible part of the selected period.",
                    evidence_ids=["e_tag_1"],
                )
            )
        if not behavior_insights:
            behavior_insights.append(
                AnalysisObservation(
                    text="The selected records support only a limited behavior insight for this period.",
                    evidence_ids=[evidence_ids[0]],
                )
            )

        output = CombinedAnalysisOutput(
            output_outcome="analysis_generated",
            generated_at=datetime.now(UTC),
            summary=summary,
            detected_patterns=detected_patterns,
            behavior_insights=behavior_insights,
            supporting_evidence=evidence,
            limitations=["Generated from task names, durations, categories, and tags only; note text was excluded."],
        )
        return AIProviderResponse(
            output=output.model_dump(mode="json"),
            provider_name=self.provider_name,
            model=request.model,
        )
