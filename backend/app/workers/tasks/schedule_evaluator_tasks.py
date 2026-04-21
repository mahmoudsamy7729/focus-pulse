"""Celery task placeholders for Phase 6 due-window evaluation."""

from __future__ import annotations

from app.workers.celery_app import celery_app


def evaluate_due_schedules_payload() -> dict[str, object]:
    return {"evaluated": False, "reason": "phase_6_placeholder"}


if celery_app is not None:

    @celery_app.task(name="workers.evaluate_due_schedules")
    def evaluate_due_schedules() -> dict[str, object]:
        return evaluate_due_schedules_payload()

else:

    class _EvaluateDueSchedulesFallback:
        def delay(self) -> dict[str, object]:
            return evaluate_due_schedules_payload()

    evaluate_due_schedules = _EvaluateDueSchedulesFallback()
