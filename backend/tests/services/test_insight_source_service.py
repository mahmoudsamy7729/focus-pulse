from datetime import date
from uuid import uuid4

from app.modules.ai_insights.models import AIInsightRun
from app.modules.ai_insights.services.insight_source_service import InsightSourceService
from app.shared.enums.run_status import RunStatus


def test_source_service_builds_period_snapshot_and_phase4_evidence() -> None:
    run = AIInsightRun(
        id=uuid4(),
        owner_id=uuid4(),
        target_period_type="weekly",
        period_start=date(2026, 4, 13),
        period_end=date(2026, 4, 19),
        status=RunStatus.COMPLETED.value,
        source_summary={
            "daily_log_count": 2,
            "task_count": 3,
            "total_minutes": 180,
            "daily_totals": [{"date": "2026-04-13", "total_minutes": 120}, {"date": "2026-04-14", "total_minutes": 60}],
            "category_totals": [{"label": "Build", "total_minutes": 180}],
        },
        output_summary={"detected_patterns": [{"text": "Build work dominated.", "evidence_ids": ["category-1"]}]},
        output_outcome="analysis_generated",
        failure_details=[],
    )

    snapshot, evidence = InsightSourceService(None).build_snapshot_and_evidence(run)  # type: ignore[arg-type]

    assert snapshot.tracked_day_count == 2
    assert snapshot.excluded_fields == ["note_text"]
    assert any(item.evidence_type == "phase4_pattern" for item in evidence)
