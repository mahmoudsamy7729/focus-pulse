from __future__ import annotations

from app.modules.ai_insights.constants import InsightConfidence, InsightScoreState
from app.modules.ai_insights.schemas import DayFinding, Recommendation, ScoreOutcome, SourceSnapshot


class RecommendationService:
    def recommend(
        self,
        snapshot: SourceSnapshot,
        productivity_score: ScoreOutcome,
        consistency_score: ScoreOutcome | None,
        best_day_finding: DayFinding | None,
        worst_day_finding: DayFinding | None,
    ) -> list[Recommendation]:
        recommendations: list[Recommendation] = []
        if productivity_score.state == InsightScoreState.INSUFFICIENT_DATA.value:
            return []
        if productivity_score.limiting_factors:
            factor = productivity_score.limiting_factors[0]
            recommendations.append(
                Recommendation(
                    recommendation_id="rec-1",
                    priority=1,
                    action="Add one short tracking check at the end of the next work session.",
                    rationale=factor.explanation,
                    expected_benefit="This should make the next score easier to explain from saved facts.",
                    confidence=InsightConfidence.MEDIUM.value,
                    evidence_ids=factor.evidence_ids,
                    source_links=["productivity_score"],
                    dedupe_key="improve-tracking-coverage",
                )
            )
        if worst_day_finding and worst_day_finding.finding_type == "worst_day":
            recommendations.append(
                Recommendation(
                    recommendation_id=f"rec-{len(recommendations) + 1}",
                    priority=len(recommendations) + 1,
                    action=f"Review the plan for {worst_day_finding.date.isoformat()} and choose one reusable setup step for similar days.",
                    rationale=worst_day_finding.summary,
                    expected_benefit="A small setup step may reduce the gap between lighter and stronger tracked days.",
                    confidence=worst_day_finding.confidence,
                    evidence_ids=worst_day_finding.evidence_ids,
                    source_links=["worst_day_finding"],
                    dedupe_key="review-lightest-day-setup",
                )
            )
        if snapshot.category_totals and len(recommendations) < 3:
            top = snapshot.category_totals[0]
            recommendations.append(
                Recommendation(
                    recommendation_id=f"rec-{len(recommendations) + 1}",
                    priority=len(recommendations) + 1,
                    action=f"Protect a focused block for {top.label} before adding smaller tasks.",
                    rationale=f"{top.label} is the strongest category signal in this result.",
                    expected_benefit="Keeping that block visible may preserve the strongest tracked pattern.",
                    confidence=InsightConfidence.MEDIUM.value,
                    evidence_ids=["category-1"],
                    source_links=["source_snapshot.category_totals"],
                    dedupe_key=f"protect-category-{top.label.lower().replace(' ', '-')}",
                )
            )
        if consistency_score and consistency_score.state == InsightScoreState.SCORED.value and consistency_score.score is not None and consistency_score.score < 55 and len(recommendations) < 3:
            recommendations.append(
                Recommendation(
                    recommendation_id=f"rec-{len(recommendations) + 1}",
                    priority=len(recommendations) + 1,
                    action="Choose a minimum daily tracking target for the next comparable week.",
                    rationale=consistency_score.summary,
                    expected_benefit="A small minimum target may make daily totals easier to compare.",
                    confidence=InsightConfidence.LOW.value,
                    evidence_ids=consistency_score.evidence_ids[:2],
                    source_links=["consistency_score"],
                    dedupe_key="minimum-daily-tracking-target",
                )
            )
        return recommendations[:3]
