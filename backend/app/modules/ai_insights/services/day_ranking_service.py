from __future__ import annotations

from app.modules.ai_insights.constants import InsightConfidence
from app.modules.ai_insights.schemas import DayFinding, SourceSnapshot


class DayRankingService:
    def rank(self, snapshot: SourceSnapshot) -> tuple[DayFinding | None, DayFinding | None]:
        if snapshot.period_granularity != "weekly":
            return None, None
        tracked = [item for item in snapshot.daily_totals if item.total_minutes > 0]
        if len(tracked) < 3:
            return None, None
        ordered = sorted(tracked, key=lambda item: (item.total_minutes, item.date))
        lowest = ordered[0]
        highest = ordered[-1]
        difference = highest.total_minutes - lowest.total_minutes
        close = difference < max(30, round(highest.total_minutes * 0.15))
        if close:
            return (
                DayFinding(
                    finding_type="no_meaningful_distinction",
                    date=None,
                    label="No clear best or worst day",
                    summary="Tracked daily totals are close enough that a best/worst label would overstate the difference.",
                    confidence=InsightConfidence.LOW.value,
                    evidence_ids=[f"date-{highest.date.isoformat()}", f"date-{lowest.date.isoformat()}"],
                    tie_or_close_ranking=True,
                ),
                None,
            )
        return (
            DayFinding(
                finding_type="best_day",
                date=highest.date,
                label="Highest tracked day",
                summary=f"{highest.date.isoformat()} had the highest tracked total at {highest.total_minutes} minutes.",
                confidence=InsightConfidence.MEDIUM.value,
                evidence_ids=[f"date-{highest.date.isoformat()}"],
                tie_or_close_ranking=False,
            ),
            DayFinding(
                finding_type="worst_day",
                date=lowest.date,
                label="Lightest tracked day",
                summary=f"{lowest.date.isoformat()} had the lightest tracked total at {lowest.total_minutes} minutes.",
                confidence=InsightConfidence.MEDIUM.value,
                evidence_ids=[f"date-{lowest.date.isoformat()}"],
                tie_or_close_ranking=False,
            ),
        )
