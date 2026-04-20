from datetime import date
from uuid import uuid4

from app.modules.ai_insights.services.insight_validation_service import InsightValidationService
from app.modules.ai_insights.services.recommendation_service import RecommendationService
from app.modules.ai_insights.schemas import (
    InsightEvidence,
    NamedMinuteTotal,
    Recommendation,
    ScoreFactor,
    ScoreOutcome,
    SourceSnapshot,
)


def test_recommendations_are_capped_and_evidence_backed() -> None:
    snapshot = SourceSnapshot(
        period_granularity="weekly",
        period_start=date(2026, 4, 13),
        period_end=date(2026, 4, 19),
        source_ai_insight_run_id=uuid4(),
        tracked_day_count=3,
        task_count=4,
        total_minutes=240,
        category_totals=[NamedMinuteTotal(label="Build", total_minutes=180)],
    )
    score = ScoreOutcome(
        score_type="productivity",
        state="scored",
        score=70,
        confidence="medium",
        summary="Scored",
        positive_factors=[],
        limiting_factors=[ScoreFactor(label="Sparse tracking", direction="limiting", explanation="Only one day had tracked work.", evidence_ids=["task-count"])],
        evidence_ids=["task-count", "category-1"],
    )
    recommendations = RecommendationService().recommend(snapshot, score, None, None, None)

    assert 0 < len(recommendations) <= 3
    assert all(recommendation.evidence_ids for recommendation in recommendations)


def test_validation_rejects_duplicate_recommendation_keys() -> None:
    snapshot = SourceSnapshot(
        period_granularity="daily",
        period_start=date(2026, 4, 15),
        period_end=date(2026, 4, 15),
        source_ai_insight_run_id=uuid4(),
        tracked_day_count=1,
        task_count=1,
        total_minutes=60,
    )
    evidence = [InsightEvidence(evidence_id="task-count", evidence_type="task_count", count=1, summary="One task.")]
    score = ScoreOutcome(
        score_type="productivity",
        state="scored",
        score=50,
        confidence="medium",
        summary="Scored",
        positive_factors=[],
        limiting_factors=[],
        evidence_ids=["task-count", "task-count"],
    )
    first = [
        Recommendation(
            recommendation_id="rec-1",
            priority=1,
            action="Add one short planning check before starting work.",
            rationale="One tracked task supports this action.",
            expected_benefit="This may make the next result easier to compare.",
            confidence="medium",
            evidence_ids=["task-count"],
            source_links=["productivity_score"],
            dedupe_key="same-key",
        ),
        Recommendation(
            recommendation_id="rec-2",
            priority=2,
            action="Add one short planning check before starting work.",
            rationale="One tracked task supports this action.",
            expected_benefit="This may make the next result easier to compare.",
            confidence="medium",
            evidence_ids=["task-count"],
            source_links=["productivity_score"],
            dedupe_key="same-key",
        ),
    ]

    outcome = InsightValidationService().validate(snapshot, score, None, None, None, first, evidence)

    assert outcome.passed is False
    assert "recommendation_quality" in outcome.failure_codes
