from datetime import date
from uuid import uuid4

from app.modules.ai_insights.models import AIInsightRun
from app.modules.ai_insights.services.insight_source_service import InsightSourceService
from app.shared.enums.run_status import RunStatus


def test_source_snapshot_and_evidence_do_not_include_note_text() -> None:
    run = AIInsightRun(
        id=uuid4(),
        owner_id=uuid4(),
        target_period_type="daily",
        period_start=date(2026, 4, 15),
        period_end=date(2026, 4, 15),
        status=RunStatus.COMPLETED.value,
        source_summary={"task_count": 1, "total_minutes": 45, "daily_totals": [{"date": "2026-04-15", "total_minutes": 45}]},
        output_summary={"detected_patterns": []},
        output_outcome="analysis_generated",
        failure_details=[],
    )

    snapshot, evidence = InsightSourceService(None).build_snapshot_and_evidence(run)  # type: ignore[arg-type]
    serialized = f"{snapshot.model_dump(mode='json')} {[item.model_dump(mode='json') for item in evidence]}"

    assert "note_text" in snapshot.excluded_fields
    assert "note content" not in serialized.lower()
