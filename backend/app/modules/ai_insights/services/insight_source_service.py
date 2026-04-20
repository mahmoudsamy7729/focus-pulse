from __future__ import annotations

from datetime import date
from uuid import UUID

from app.modules.ai_insights.constants import AIInsightOutputOutcome
from app.modules.ai_insights.exceptions import InvalidSourceAnalysisError, MissingSourceAnalysisError
from app.modules.ai_insights.models import AIInsightRun
from app.modules.ai_insights.repositories.ai_insight_run_repository import AIInsightRunRepository
from app.modules.ai_insights.schemas import DailyMinuteTotal, InsightEvidence, NamedMinuteTotal, SourceSnapshot
from app.shared.enums.run_status import RunStatus


class InsightSourceService:
    def __init__(self, run_repository: AIInsightRunRepository) -> None:
        self.run_repository = run_repository

    async def resolve_source_analysis(
        self,
        owner_id: UUID,
        period_granularity: str,
        period_start: date,
        period_end: date,
        source_ai_insight_run_id: UUID | None = None,
    ) -> AIInsightRun:
        source = await self.run_repository.find_completed_source_analysis(
            owner_id,
            period_granularity,
            period_start,
            period_end,
            source_ai_insight_run_id,
        )
        if source is None:
            if source_ai_insight_run_id is not None:
                raise InvalidSourceAnalysisError("Selected source analysis is not completed for this owner and period.")
            raise MissingSourceAnalysisError("No completed source analysis exists for this owner and period.")
        if source.status != RunStatus.COMPLETED.value or source.output_summary is None:
            raise InvalidSourceAnalysisError("Source analysis must be completed and have output.")
        if source.output_outcome not in {AIInsightOutputOutcome.ANALYSIS_GENERATED.value, AIInsightOutputOutcome.NO_DATA.value}:
            raise InvalidSourceAnalysisError("Source analysis output outcome is not usable.")
        return source

    def build_snapshot_and_evidence(self, source: AIInsightRun) -> tuple[SourceSnapshot, list[InsightEvidence]]:
        summary = dict(source.source_summary or {})
        output = dict(source.output_summary or {})
        daily_totals = self._daily_totals(summary.get("daily_totals"))
        tracked_day_count = sum(1 for item in daily_totals if item.total_minutes > 0)
        source_daily_log_ids = [UUID(str(value)) for value in summary.get("source_daily_log_ids", [])]
        phase4_observation_ids = self._phase4_observation_ids(output)
        snapshot = SourceSnapshot(
            period_granularity=source.target_period_type,  # type: ignore[arg-type]
            period_start=source.period_start,
            period_end=source.period_end,
            source_ai_insight_run_id=source.id,
            source_daily_log_ids=source_daily_log_ids,
            source_task_ids=[],
            daily_log_count=int(summary.get("daily_log_count") or len(source_daily_log_ids)),
            tracked_day_count=tracked_day_count,
            task_count=int(summary.get("task_count") or 0),
            total_minutes=int(summary.get("total_minutes") or 0),
            category_totals=self._named_totals(summary.get("category_totals")),
            tag_totals=self._named_totals(summary.get("tag_totals")),
            daily_totals=daily_totals,
            phase4_observation_ids=phase4_observation_ids,
            included_fields=list(summary.get("included_fields") or ["task_names", "durations", "categories", "tags"]),
            excluded_fields=sorted(set(list(summary.get("excluded_fields") or []) + ["note_text"])),
        )
        return snapshot, self._build_evidence(source, snapshot, output)

    @staticmethod
    def _named_totals(raw: object) -> list[NamedMinuteTotal]:
        if not isinstance(raw, list):
            return []
        totals: list[NamedMinuteTotal] = []
        for item in raw:
            if isinstance(item, dict):
                totals.append(NamedMinuteTotal(label=str(item.get("label") or "Uncategorized"), total_minutes=int(item.get("total_minutes") or 0)))
        return totals

    @staticmethod
    def _daily_totals(raw: object) -> list[DailyMinuteTotal]:
        if not isinstance(raw, list):
            return []
        totals: list[DailyMinuteTotal] = []
        for item in raw:
            if isinstance(item, dict) and item.get("date"):
                totals.append(DailyMinuteTotal(date=date.fromisoformat(str(item["date"])), total_minutes=int(item.get("total_minutes") or 0)))
        return totals

    @staticmethod
    def _phase4_observation_ids(output: dict[str, object]) -> list[str]:
        identifiers: list[str] = []
        for prefix, key in (("pattern", "detected_patterns"), ("behavior", "behavior_insights")):
            values = output.get(key)
            if isinstance(values, list):
                identifiers.extend(f"{prefix}-{index}" for index, _ in enumerate(values, start=1))
        return identifiers

    def _build_evidence(self, source: AIInsightRun, snapshot: SourceSnapshot, output: dict[str, object]) -> list[InsightEvidence]:
        evidence: list[InsightEvidence] = []
        if snapshot.task_count:
            evidence.append(
                InsightEvidence(
                    evidence_id="task-count",
                    evidence_type="task_count",
                    count=snapshot.task_count,
                    summary=f"{snapshot.task_count} tracked tasks in the selected period.",
                )
            )
        for item in snapshot.daily_totals:
            if item.total_minutes > 0:
                evidence.append(
                    InsightEvidence(
                        evidence_id=f"date-{item.date.isoformat()}",
                        evidence_type="date_total",
                        source_date=item.date,
                        minutes=item.total_minutes,
                        summary=f"{item.total_minutes} minutes tracked on {item.date.isoformat()}.",
                    )
                )
        for index, item in enumerate(snapshot.category_totals[:3], start=1):
            evidence.append(
                InsightEvidence(
                    evidence_id=f"category-{index}",
                    evidence_type="category_total",
                    label=item.label,
                    minutes=item.total_minutes,
                    summary=f"{item.label} accounts for {item.total_minutes} tracked minutes.",
                )
            )
        for index, item in enumerate(snapshot.tag_totals[:3], start=1):
            evidence.append(
                InsightEvidence(
                    evidence_id=f"tag-{index}",
                    evidence_type="tag_total",
                    label=item.label,
                    minutes=item.total_minutes,
                    summary=f"{item.label} accounts for {item.total_minutes} tagged minutes.",
                )
            )
        evidence.extend(self._phase4_evidence(source, output))
        return evidence

    @staticmethod
    def _phase4_evidence(source: AIInsightRun, output: dict[str, object]) -> list[InsightEvidence]:
        evidence: list[InsightEvidence] = []
        for prefix, key, evidence_type in (
            ("pattern", "detected_patterns", "phase4_pattern"),
            ("behavior", "behavior_insights", "phase4_behavior_insight"),
        ):
            values = output.get(key)
            if not isinstance(values, list):
                continue
            for index, item in enumerate(values, start=1):
                if isinstance(item, dict):
                    text = str(item.get("text") or "").strip()
                    if text:
                        evidence.append(
                            InsightEvidence(
                                evidence_id=f"{prefix}-{index}",
                                evidence_type=evidence_type,  # type: ignore[arg-type]
                                source_ai_insight_run_id=source.id,
                                source_observation_id=f"{prefix}-{index}",
                                summary=text,
                            )
                        )
        return evidence
