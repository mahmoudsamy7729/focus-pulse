from __future__ import annotations

from datetime import UTC, datetime

from app.modules.ai_insights.constants import INSIGHT_VALIDATOR_VERSION, InsightScoreState, InsightValidationCode
from app.modules.ai_insights.schemas import (
    DayFinding,
    InsightEvidence,
    InsightValidationCheck,
    InsightValidationOutcome,
    Recommendation,
    ScoreOutcome,
    SourceSnapshot,
)


class InsightValidationService:
    BLOCKED_WORDS = {"lazy", "failure", "diagnose", "medical", "depression", "adhd", "character"}

    def validate(
        self,
        snapshot: SourceSnapshot,
        productivity_score: ScoreOutcome,
        consistency_score: ScoreOutcome | None,
        best_day_finding: DayFinding | None,
        worst_day_finding: DayFinding | None,
        recommendations: list[Recommendation],
        evidence: list[InsightEvidence],
    ) -> InsightValidationOutcome:
        evidence_ids = {item.evidence_id for item in evidence}
        checks = [
            self._check(InsightValidationCode.SOURCE_PERIOD_MATCH.value, snapshot.period_start <= snapshot.period_end),
            self._check(InsightValidationCode.PRIVACY_BOUNDARY.value, "note_text" in snapshot.excluded_fields),
            self._check(InsightValidationCode.SCORE_BOUNDS.value, self._score_bounds(productivity_score) and self._score_bounds(consistency_score)),
            self._check(
                InsightValidationCode.SCORE_EVIDENCE.value,
                self._score_evidence(productivity_score, evidence_ids) and self._score_evidence(consistency_score, evidence_ids),
            ),
            self._check(
                InsightValidationCode.DAY_FINDING_EVIDENCE.value,
                self._finding_evidence(best_day_finding, evidence_ids) and self._finding_evidence(worst_day_finding, evidence_ids),
            ),
            self._check(InsightValidationCode.RECOMMENDATION_COUNT.value, len(recommendations) <= 3),
            self._check(InsightValidationCode.RECOMMENDATION_QUALITY.value, self._recommendation_quality(recommendations, evidence_ids)),
        ]
        failures = [check.code for check in checks if check.blocking and not check.passed]
        return InsightValidationOutcome(
            passed=not failures,
            checked_at=datetime.now(UTC),
            validator_version=INSIGHT_VALIDATOR_VERSION,
            checks=checks,
            failure_codes=failures,
        )

    @staticmethod
    def _check(code: str, passed: bool) -> InsightValidationCheck:
        return InsightValidationCheck(code=code, passed=passed, blocking=True)

    @staticmethod
    def _score_bounds(score: ScoreOutcome | None) -> bool:
        if score is None:
            return True
        if score.state == InsightScoreState.SCORED.value:
            return score.score is not None and 0 <= score.score <= 100
        return score.score is None

    @staticmethod
    def _score_evidence(score: ScoreOutcome | None, evidence_ids: set[str]) -> bool:
        if score is None or score.state != InsightScoreState.SCORED.value:
            return True
        return len(score.evidence_ids) >= 2 and set(score.evidence_ids).issubset(evidence_ids)

    @staticmethod
    def _finding_evidence(finding: DayFinding | None, evidence_ids: set[str]) -> bool:
        if finding is None:
            return True
        return set(finding.evidence_ids).issubset(evidence_ids)

    def _recommendation_quality(self, recommendations: list[Recommendation], evidence_ids: set[str]) -> bool:
        seen: set[str] = set()
        for recommendation in recommendations:
            text = " ".join([recommendation.action, recommendation.rationale, recommendation.expected_benefit]).lower()
            if recommendation.dedupe_key in seen or not set(recommendation.evidence_ids).issubset(evidence_ids):
                return False
            if any(word in text for word in self.BLOCKED_WORDS):
                return False
            if len(recommendation.action.split()) < 4:
                return False
            seen.add(recommendation.dedupe_key)
        return True
