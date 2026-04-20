from __future__ import annotations

from statistics import mean

from app.modules.ai_insights.constants import InsightConfidence, InsightScoreState
from app.modules.ai_insights.schemas import InsightEvidence, ScoreFactor, ScoreOutcome, SourceSnapshot


class ConsistencyScoringService:
    def score(self, snapshot: SourceSnapshot, evidence: list[InsightEvidence]) -> ScoreOutcome:
        if snapshot.period_granularity == "daily":
            return ScoreOutcome(
                score_type="consistency",
                state=InsightScoreState.NOT_APPLICABLE.value,
                score=None,
                confidence=InsightConfidence.LOW.value,
                summary="Consistency is only calculated for weekly insight periods.",
                positive_factors=[],
                limiting_factors=[],
                evidence_ids=[],
                insufficient_data_reason="Daily periods do not support consistency scoring.",
            )
        non_zero = [item.total_minutes for item in snapshot.daily_totals if item.total_minutes > 0]
        evidence_ids = [f"date-{item.date.isoformat()}" for item in snapshot.daily_totals if item.total_minutes > 0][:4]
        if len(non_zero) < 3:
            return ScoreOutcome(
                score_type="consistency",
                state=InsightScoreState.INSUFFICIENT_DATA.value,
                score=None,
                confidence=InsightConfidence.LOW.value,
                summary="At least three tracked days are needed to compare weekly consistency.",
                positive_factors=[],
                limiting_factors=[],
                evidence_ids=evidence_ids,
                insufficient_data_reason="Weekly consistency requires at least three tracked days.",
            )
        avg = mean(non_zero)
        spread = max(non_zero) - min(non_zero)
        score = max(0, min(100, round(100 - min(spread / max(avg, 1), 1) * 55)))
        factors = [
            ScoreFactor(
                label="Tracked day coverage",
                direction="positive",
                explanation=f"{len(non_zero)} days in the selected week include tracked work.",
                evidence_ids=evidence_ids[:2],
            )
        ]
        limiting = []
        if spread > avg:
            limiting.append(
                ScoreFactor(
                    label="Uneven daily totals",
                    direction="limiting",
                    explanation="The difference between the highest and lowest tracked days lowers consistency.",
                    evidence_ids=evidence_ids[:2],
                )
            )
        return ScoreOutcome(
            score_type="consistency",
            state=InsightScoreState.SCORED.value,
            score=score,
            confidence=InsightConfidence.HIGH.value if len(non_zero) >= 5 else InsightConfidence.MEDIUM.value,
            summary=f"Weekly consistency score is {score} based on {len(non_zero)} tracked days.",
            positive_factors=factors,
            limiting_factors=limiting,
            evidence_ids=evidence_ids,
        )
