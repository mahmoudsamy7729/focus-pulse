from datetime import UTC, date, datetime
from uuid import uuid4

from app.modules.ai_insights.models import AIInsightResult, AIInsightResultSource


def test_ai_insight_result_model_defaults_and_source_relationship_shape() -> None:
    owner_id = uuid4()
    run_id = uuid4()
    result = AIInsightResult(
        owner_id=owner_id,
        period_granularity="daily",
        period_start=date(2026, 4, 15),
        period_end=date(2026, 4, 15),
        source_ai_insight_run_id=run_id,
        status="completed",
        is_current=True,
        generation_reason="default_generate",
        source_snapshot={"excluded_fields": ["note_text"]},
        productivity_score={"state": "insufficient_data"},
        recommendations=[],
        evidence=[],
        validation_outcome={"passed": True},
        generated_at=datetime.now(UTC),
    )
    source = AIInsightResultSource(owner_id=owner_id, ai_insight_result_id=uuid4(), daily_log_id=uuid4(), created_at=datetime.now(UTC))

    assert result.status == "completed"
    assert result.deleted_at is None
    assert source.owner_id == owner_id
