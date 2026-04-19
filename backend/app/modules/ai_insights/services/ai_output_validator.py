from __future__ import annotations

import json

from pydantic import ValidationError

from app.modules.ai_insights.constants import AIInsightOutputOutcome
from app.modules.ai_insights.exceptions import AIOutputValidationError
from app.modules.ai_insights.schemas import CombinedAnalysisOutput, StructuredAIInput


class AIOutputValidator:
    def validate_output(
        self,
        output: dict[str, object],
        provider_input: StructuredAIInput,
        *,
        forbidden_text: list[str] | None = None,
    ) -> CombinedAnalysisOutput:
        self._ensure_note_text_absent(output, forbidden_text or [])
        try:
            parsed = CombinedAnalysisOutput.model_validate(output)
        except ValidationError as exc:
            raise AIOutputValidationError("AI output did not match the combined output schema.") from exc

        if parsed.output_outcome == AIInsightOutputOutcome.NO_DATA.value:
            if parsed.summary or parsed.detected_patterns or parsed.behavior_insights or parsed.supporting_evidence:
                raise AIOutputValidationError("no_data outputs must not include analysis claims.")
            return parsed

        if parsed.output_outcome != AIInsightOutputOutcome.ANALYSIS_GENERATED.value:
            raise AIOutputValidationError("output_outcome is unsupported.")
        if not parsed.summary or not parsed.summary.strip():
            raise AIOutputValidationError("analysis_generated outputs require summary.")
        if provider_input.tasks and not parsed.supporting_evidence:
            raise AIOutputValidationError("analysis_generated outputs require supporting evidence.")

        evidence_ids = {item.evidence_id for item in parsed.supporting_evidence}
        for observation in [*parsed.detected_patterns, *parsed.behavior_insights]:
            missing_ids = [evidence_id for evidence_id in observation.evidence_ids if evidence_id not in evidence_ids]
            if missing_ids:
                raise AIOutputValidationError("observation references unknown supporting evidence.")
        return parsed

    @staticmethod
    def _ensure_note_text_absent(output: dict[str, object], forbidden_text: list[str]) -> None:
        serialized = json.dumps(output, default=str).lower()
        for value in forbidden_text:
            if value and value.lower() in serialized:
                raise AIOutputValidationError("AI output contains excluded note text.")
