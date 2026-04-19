from datetime import UTC, date, datetime
from uuid import uuid4

import pytest

from app.modules.ai_insights.exceptions import AIOutputValidationError
from app.modules.ai_insights.schemas import AnalysisInputSummary, StructuredAIInput, StructuredTaskInput
from app.modules.ai_insights.services.ai_output_validator import AIOutputValidator


def _provider_input() -> StructuredAIInput:
    return StructuredAIInput(
        period_granularity="daily",
        period_start=date(2026, 4, 15),
        period_end=date(2026, 4, 15),
        tasks=[
            StructuredTaskInput(
                task_id=uuid4(),
                daily_log_id=uuid4(),
                date=date(2026, 4, 15),
                title="Plan",
                minutes=30,
                category="Work",
                tags=["planning"],
            )
        ],
        aggregates=AnalysisInputSummary(task_count=1, total_minutes=30),
        instruction_name="daily_combined_analysis",
        instruction_version="test",
    )


def test_output_validator_accepts_evidence_backed_combined_output() -> None:
    output = {
        "output_outcome": "analysis_generated",
        "generated_at": datetime.now(UTC).isoformat(),
        "summary": "Tracked one planning task.",
        "detected_patterns": [{"text": "Planning was present.", "evidence_ids": ["e1"]}],
        "behavior_insights": [{"text": "Work received focused time.", "evidence_ids": ["e1"]}],
        "supporting_evidence": [{"evidence_id": "e1", "evidence_type": "task_count", "count": 1}],
        "limitations": ["Notes excluded."],
    }

    parsed = AIOutputValidator().validate_output(output, _provider_input())

    assert parsed.output_outcome == "analysis_generated"


def test_output_validator_rejects_unknown_evidence_and_note_leakage() -> None:
    output = {
        "output_outcome": "analysis_generated",
        "generated_at": datetime.now(UTC).isoformat(),
        "summary": "Secret note text appears here.",
        "detected_patterns": [{"text": "Unsupported.", "evidence_ids": ["missing"]}],
        "behavior_insights": [],
        "supporting_evidence": [{"evidence_id": "e1", "evidence_type": "task_count", "count": 1}],
        "limitations": [],
    }

    with pytest.raises(AIOutputValidationError):
        AIOutputValidator().validate_output(output, _provider_input(), forbidden_text=["secret note text"])
