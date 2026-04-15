from datetime import UTC, date, datetime
from uuid import UUID

from app.modules.imports.constants import IMPORT_ROW_OUTCOME_TYPES, ImportRowOutcomeType
from app.modules.imports.exceptions import InvalidImportOutcomeError, InvalidImportStatusTransitionError
from app.modules.imports.models import ImportRowOutcome, ImportRun
from app.modules.imports.repositories.import_run_repository import ImportRunRepository
from app.shared.enums.run_status import RunStatus, VALID_RUN_TRANSITIONS


class ImportTraceService:
    def __init__(self, repository: ImportRunRepository) -> None:
        self.repository = repository

    async def create_import_run(self, owner_id: UUID, source_type: str, source_name: str) -> ImportRun:
        return await self.repository.add(
            ImportRun(
                owner_id=owner_id,
                source_type=source_type,
                source_name=source_name,
                status=RunStatus.PENDING.value,
            )
        )

    async def mark_import_processing(self, import_run_id: UUID) -> ImportRun:
        import_run = await self._get_required(import_run_id)
        self._ensure_transition(import_run.status, RunStatus.PROCESSING.value)
        import_run.status = RunStatus.PROCESSING.value
        import_run.started_at = datetime.now(UTC)
        return import_run

    async def record_inserted_row(self, import_run_id: UUID, count: int = 1) -> ImportRun:
        import_run = await self._get_required(import_run_id)
        import_run.inserted_row_count += count
        import_run.processed_row_count += count
        return import_run

    async def record_import_row_outcome(
        self,
        import_run_id: UUID,
        row_number: int | None,
        outcome_type: str,
        reason: str,
        row_summary: dict[str, object] | None = None,
    ) -> ImportRowOutcome:
        if outcome_type not in IMPORT_ROW_OUTCOME_TYPES:
            raise InvalidImportOutcomeError(f"unsupported import row outcome: {outcome_type}")

        import_run = await self._get_required(import_run_id)
        if not reason.strip():
            raise InvalidImportOutcomeError("reason must not be empty")

        summary = row_summary or {}
        raw_log_date = summary.get("log_date")
        log_date = date.fromisoformat(raw_log_date) if isinstance(raw_log_date, str) else raw_log_date
        row_outcome = await self.repository.add_row_outcome(
            ImportRowOutcome(
                owner_id=import_run.owner_id,
                import_run_id=import_run.id,
                row_number=row_number,
                outcome_type=outcome_type,
                reason=reason.strip(),
                normalized_task_name=summary.get("normalized_task_name"),
                log_date=log_date,
                time_spent_minutes=summary.get("time_spent_minutes"),
                row_snapshot=summary,
                created_at=datetime.now(UTC),
            )
        )
        import_run.processed_row_count += 1
        if outcome_type == ImportRowOutcomeType.INVALID.value:
            import_run.invalid_row_count += 1
        elif outcome_type == ImportRowOutcomeType.SKIPPED.value:
            import_run.skipped_row_count += 1
        elif outcome_type == ImportRowOutcomeType.FAILED.value:
            import_run.failed_row_count += 1
        return row_outcome

    async def complete_import_run(
        self,
        import_run_id: UUID,
        status: str,
        failure_reason: str | None = None,
    ) -> ImportRun:
        import_run = await self._get_required(import_run_id)
        self._ensure_transition(import_run.status, status)
        if status == RunStatus.FAILED.value and not (failure_reason or "").strip():
            raise InvalidImportStatusTransitionError("failed import runs require failure_reason")
        import_run.status = status
        import_run.failure_reason = failure_reason
        import_run.completed_at = datetime.now(UTC)
        return import_run

    async def _get_required(self, import_run_id: UUID) -> ImportRun:
        import_run = await self.repository.get(import_run_id)
        if import_run is None:
            raise InvalidImportStatusTransitionError("import run not found")
        return import_run

    @staticmethod
    def _ensure_transition(current_status: str, next_status: str) -> None:
        allowed = VALID_RUN_TRANSITIONS.get(RunStatus(current_status), set())
        if RunStatus(next_status) not in allowed:
            raise InvalidImportStatusTransitionError(f"invalid status transition: {current_status} -> {next_status}")
