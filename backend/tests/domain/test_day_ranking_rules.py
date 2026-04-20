from datetime import date
from uuid import uuid4

from app.modules.ai_insights.services.day_ranking_service import DayRankingService
from app.modules.ai_insights.schemas import DailyMinuteTotal, SourceSnapshot


def test_weekly_day_ranking_identifies_best_and_lightest_days_neutrally() -> None:
    snapshot = SourceSnapshot(
        period_granularity="weekly",
        period_start=date(2026, 4, 13),
        period_end=date(2026, 4, 19),
        source_ai_insight_run_id=uuid4(),
        tracked_day_count=3,
        task_count=3,
        total_minutes=270,
        daily_totals=[
            DailyMinuteTotal(date=date(2026, 4, 13), total_minutes=180),
            DailyMinuteTotal(date=date(2026, 4, 14), total_minutes=60),
            DailyMinuteTotal(date=date(2026, 4, 15), total_minutes=30),
        ],
    )

    best, worst = DayRankingService().rank(snapshot)

    assert best is not None and best.finding_type == "best_day"
    assert worst is not None and worst.finding_type == "worst_day"
    assert "lightest" in worst.summary.lower()


def test_weekly_day_ranking_explains_close_totals_without_overstating() -> None:
    snapshot = SourceSnapshot(
        period_granularity="weekly",
        period_start=date(2026, 4, 13),
        period_end=date(2026, 4, 19),
        source_ai_insight_run_id=uuid4(),
        tracked_day_count=3,
        task_count=3,
        total_minutes=300,
        daily_totals=[
            DailyMinuteTotal(date=date(2026, 4, 13), total_minutes=100),
            DailyMinuteTotal(date=date(2026, 4, 14), total_minutes=105),
            DailyMinuteTotal(date=date(2026, 4, 15), total_minutes=110),
        ],
    )

    best, worst = DayRankingService().rank(snapshot)

    assert best is not None
    assert best.finding_type == "no_meaningful_distinction"
    assert best.tie_or_close_ranking is True
    assert worst is None
