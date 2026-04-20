from datetime import date
from uuid import uuid4

from app.modules.ai_insights.services.consistency_scoring_service import ConsistencyScoringService
from app.modules.ai_insights.services.productivity_scoring_service import ProductivityScoringService
from app.modules.ai_insights.schemas import DailyMinuteTotal, InsightEvidence, NamedMinuteTotal, SourceSnapshot


def _snapshot(tracked_days: int = 3) -> SourceSnapshot:
    daily_totals = [
        DailyMinuteTotal(date=date(2026, 4, 13), total_minutes=120),
        DailyMinuteTotal(date=date(2026, 4, 14), total_minutes=90),
        DailyMinuteTotal(date=date(2026, 4, 15), total_minutes=60 if tracked_days >= 3 else 0),
    ]
    return SourceSnapshot(
        period_granularity="weekly",
        period_start=date(2026, 4, 13),
        period_end=date(2026, 4, 19),
        source_ai_insight_run_id=uuid4(),
        daily_log_count=tracked_days,
        tracked_day_count=tracked_days,
        task_count=5,
        total_minutes=sum(item.total_minutes for item in daily_totals),
        category_totals=[NamedMinuteTotal(label="Build", total_minutes=180)],
        daily_totals=daily_totals,
    )


def _evidence() -> list[InsightEvidence]:
    return [
        InsightEvidence(evidence_id="task-count", evidence_type="task_count", count=5, summary="5 tracked tasks."),
        InsightEvidence(evidence_id="date-2026-04-13", evidence_type="date_total", source_date=date(2026, 4, 13), minutes=120, summary="120 minutes."),
        InsightEvidence(evidence_id="date-2026-04-14", evidence_type="date_total", source_date=date(2026, 4, 14), minutes=90, summary="90 minutes."),
        InsightEvidence(evidence_id="category-1", evidence_type="category_total", label="Build", minutes=180, summary="Build work."),
    ]


def test_productivity_score_is_bounded_and_evidence_backed() -> None:
    score = ProductivityScoringService().score(_snapshot(), _evidence())

    assert score.state == "scored"
    assert score.score is not None
    assert 0 <= score.score <= 100
    assert len(score.evidence_ids) >= 2


def test_productivity_score_uses_insufficient_data_state() -> None:
    snapshot = _snapshot(tracked_days=0)
    snapshot.task_count = 0
    score = ProductivityScoringService().score(snapshot, [])

    assert score.state == "insufficient_data"
    assert score.score is None
    assert score.insufficient_data_reason


def test_weekly_consistency_requires_three_tracked_days() -> None:
    score = ConsistencyScoringService().score(_snapshot(tracked_days=2), _evidence())

    assert score.state == "insufficient_data"
    assert score.score is None


def test_daily_consistency_is_not_applicable() -> None:
    snapshot = _snapshot()
    snapshot.period_granularity = "daily"
    snapshot.period_end = snapshot.period_start

    score = ConsistencyScoringService().score(snapshot, _evidence())

    assert score.state == "not_applicable"
