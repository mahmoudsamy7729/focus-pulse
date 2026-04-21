"""Shared scheduler orchestration placeholders for Phase 6 automation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Protocol
from uuid import uuid4

from app.workers.schedule_windows import AutomationType, ScheduleWindow


@dataclass(frozen=True)
class SchedulerContext:
    correlation_id: str
    actor_type: str = "scheduler"
    metadata: dict[str, object] = field(default_factory=dict)


class ScheduleEvaluationService(Protocol):
    async def evaluate_due_window(
        self,
        window: ScheduleWindow,
        context: SchedulerContext,
    ) -> dict[str, object]:
        """Evaluate one due schedule window."""


def build_scheduler_correlation_id(prefix: str = "scheduler") -> str:
    return f"{prefix}-{uuid4()}"


def build_scheduler_context(
    *,
    correlation_id: str | None = None,
    metadata: dict[str, object] | None = None,
) -> SchedulerContext:
    return SchedulerContext(
        correlation_id=correlation_id or build_scheduler_correlation_id(),
        metadata=metadata or {},
    )


async def evaluate_schedule_windows(
    *,
    windows: Iterable[ScheduleWindow],
    import_service: ScheduleEvaluationService,
    ai_analysis_service: ScheduleEvaluationService,
    context: SchedulerContext | None = None,
) -> list[dict[str, object]]:
    scheduler_context = context or build_scheduler_context()
    results: list[dict[str, object]] = []
    for window in windows:
        service = _service_for_window(
            window,
            import_service=import_service,
            ai_analysis_service=ai_analysis_service,
        )
        results.append(await service.evaluate_due_window(window, scheduler_context))
    return results


def _service_for_window(
    window: ScheduleWindow,
    *,
    import_service: ScheduleEvaluationService,
    ai_analysis_service: ScheduleEvaluationService,
) -> ScheduleEvaluationService:
    if window.automation_type == AutomationType.SCHEDULED_IMPORT:
        return import_service
    if window.automation_type == AutomationType.SCHEDULED_AI_ANALYSIS:
        return ai_analysis_service
    raise ValueError(f"Unsupported automation type: {window.automation_type}")
