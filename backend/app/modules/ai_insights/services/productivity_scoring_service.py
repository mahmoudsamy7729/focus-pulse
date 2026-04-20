from __future__ import annotations

from app.modules.ai_insights.constants import InsightConfidence, InsightScoreState
from app.modules.ai_insights.schemas import InsightEvidence, ScoreFactor, ScoreOutcome, SourceSnapshot


class ProductivityScoringService:
    def score(self, snapshot: SourceSnapshot, evidence: list[InsightEvidence]) -> ScoreOutcome:
        evidence_ids = [item.evidence_id for item in evidence[:4]]
        if snapshot.tracked_day_count < 1 or snapshot.task_count < 1 or len(evidence_ids) < 2:
            return ScoreOutcome(
                score_type="productivity",
                state=InsightScoreState.INSUFFICIENT_DATA.value,
                score=None,
                confidence=InsightConfidence.LOW.value,
                summary="There is not enough tracked work and evidence to calculate a productivity score.",
                positive_factors=[],
                limiting_factors=[],
                evidence_ids=evidence_ids,
                insufficient_data_reason="At least one tracked day, one task, completed analysis, and two evidence points are required.",
            )

        avg_minutes = snapshot.total_minutes / max(snapshot.tracked_day_count, 1)
        score = round(30 + min(avg_minutes / 6, 35) + min(snapshot.task_count * 3, 20) + min(len(snapshot.category_totals) * 3, 15))
        score = max(0, min(100, score))
        positive: list[ScoreFactor] = []
        limiting: list[ScoreFactor] = []
        if snapshot.total_minutes > 0:
            positive.append(
                ScoreFactor(
                    label="Tracked work volume",
                    direction="positive",
                    explanation=f"{snapshot.total_minutes} minutes were tracked across the selected period.",
                    evidence_ids=evidence_ids[:2],
                )
            )
        if snapshot.category_totals:
            positive.append(
                ScoreFactor(
                    label="Category signal",
                    direction="positive",
                    explanation=f"{snapshot.category_totals[0].label} was the largest tracked category.",
                    evidence_ids=[evidence_ids[-1]],
                )
            )
        if snapshot.tracked_day_count <= 1 and snapshot.period_granularity == "weekly":
            limiting.append(
                ScoreFactor(
                    label="Sparse tracking",
                    direction="limiting",
                    explanation="Only one day in the week had tracked work, so the score confidence is lower.",
                    evidence_ids=evidence_ids[:1],
                )
            )
        return ScoreOutcome(
            score_type="productivity",
            state=InsightScoreState.SCORED.value,
            score=score,
            confidence=InsightConfidence.HIGH.value if snapshot.tracked_day_count >= 5 else InsightConfidence.MEDIUM.value,
            summary=f"Productivity score is {score} based on tracked minutes, task volume, and category signal.",
            positive_factors=positive,
            limiting_factors=limiting,
            evidence_ids=evidence_ids,
        )
