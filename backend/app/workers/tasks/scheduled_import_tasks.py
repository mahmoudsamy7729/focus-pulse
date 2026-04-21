"""Celery task placeholders for Phase 6 scheduled imports."""

from __future__ import annotations

from uuid import UUID

from app.workers.celery_app import celery_app


def process_scheduled_import_payload(schedule_run_id: UUID, owner_id: UUID) -> dict[str, object]:
    return {
        "processed": False,
        "reason": "phase_6_placeholder",
        "schedule_run_id": str(schedule_run_id),
        "owner_id": str(owner_id),
    }


if celery_app is not None:

    @celery_app.task(name="imports.process_scheduled_import")
    def process_scheduled_import(schedule_run_id: str, owner_id: str) -> dict[str, object]:
        return process_scheduled_import_payload(UUID(schedule_run_id), UUID(owner_id))

else:

    class _ProcessScheduledImportFallback:
        def delay(self, schedule_run_id: str, owner_id: str) -> dict[str, object]:
            return {
                "queued": False,
                "schedule_run_id": schedule_run_id,
                "owner_id": owner_id,
            }

    process_scheduled_import = _ProcessScheduledImportFallback()
