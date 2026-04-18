import logging
from collections.abc import Callable
from uuid import UUID

from app.core.logging import get_logger, log_with_request_id
from app.modules.daily_logs.services.daily_log_service import DailyLogService
from app.modules.imports.constants import CSV_SOURCE_TYPE, ImportRowOutcomeType
from app.modules.imports.exceptions import CSVValidationError, ImportEnqueueError
from app.modules.imports.schemas import (
    ConfirmedImportRequest,
    ImportAcceptedResponse,
    ImportProcessingResult,
    InvalidImportRow,
    NormalizedImportRow,
)
from app.modules.imports.services.csv_parser_service import CSVParserService
from app.modules.imports.services.import_trace_service import ImportTraceService
from app.modules.tasks.services.task_service import TaskService
from app.shared.enums.run_status import RunStatus
from app.shared.enums.source import SourceLabel

EnqueueImport = Callable[[UUID, UUID, list[dict[str, object]], list[dict[str, object]]], object]


class CSVImportService:
    def __init__(
        self,
        parser: CSVParserService,
        import_trace_service: ImportTraceService,
        daily_log_service: DailyLogService,
        task_service: TaskService,
        enqueue_import: EnqueueImport | None = None,
    ) -> None:
        self.parser = parser
        self.import_trace_service = import_trace_service
        self.daily_log_service = daily_log_service
        self.task_service = task_service
        self.enqueue_import = enqueue_import
        self.logger = get_logger(__name__)

    async def confirm_csv_import(self, command: ConfirmedImportRequest) -> ImportAcceptedResponse:
        parsed = self.parser.parse(command.csv_bytes, command.source_name)
        if not parsed.valid_rows:
            raise CSVValidationError("CSV file contains no valid rows to import.")

        import_run = await self.import_trace_service.create_import_run(
            command.owner_id,
            CSV_SOURCE_TYPE,
            command.source_name,
        )
        log_with_request_id(
            self.logger,
            logging.INFO,
            "csv import accepted",
            request_id=command.request_id,
            extra={"import_run_id": str(import_run.id), "valid_rows": len(parsed.valid_rows)},
        )

        enqueue = self.enqueue_import or self._default_enqueue
        try:
            enqueue(
                import_run.id,
                command.owner_id,
                [row.model_dump(mode="json") for row in parsed.valid_rows],
                [row.model_dump(mode="json") for row in parsed.invalid_rows],
            )
        except Exception as exc:  # noqa: BLE001 - convert queue failures to stable API error
            raise ImportEnqueueError("Confirmed import could not be enqueued.") from exc

        return ImportAcceptedResponse(import_run_id=import_run.id, status=import_run.status)

    async def process_import_payload(
        self,
        import_run_id: UUID,
        owner_id: UUID,
        valid_rows: list[NormalizedImportRow],
        invalid_rows: list[InvalidImportRow] | None = None,
    ) -> ImportProcessingResult:
        await self.import_trace_service.mark_import_processing(import_run_id)

        try:
            for invalid_row in invalid_rows or []:
                await self.import_trace_service.record_import_row_outcome(
                    import_run_id=import_run_id,
                    row_number=invalid_row.row_number,
                    outcome_type=ImportRowOutcomeType.INVALID.value,
                    reason=invalid_row.reason,
                    row_summary=invalid_row.row_snapshot,
                )

            for row in valid_rows:
                try:
                    before = await self.import_trace_service._get_required(import_run_id)
                    before_skipped = before.skipped_row_count
                    daily_log = await self.daily_log_service.get_or_create_daily_log(
                        owner_id,
                        row.log_date,
                        source=SourceLabel.CSV_IMPORT.value,
                    )
                    task = await self.task_service.create_task(
                        owner_id=owner_id,
                        daily_log=daily_log,
                        title=row.task_name,
                        time_spent_minutes=row.time_spent_minutes,
                        category_name=row.category_name,
                        tags=row.tags,
                        note=row.note,
                        import_run_id=import_run_id,
                        row_number=row.row_number,
                        row_snapshot=row.row_snapshot,
                    )
                    after = await self.import_trace_service._get_required(import_run_id)
                    if task.import_run_id == import_run_id and after.skipped_row_count == before_skipped:
                        await self.import_trace_service.record_inserted_row(import_run_id)
                except Exception as exc:  # noqa: BLE001 - row-level isolation is intentional
                    await self.import_trace_service.record_import_row_outcome(
                        import_run_id=import_run_id,
                        row_number=row.row_number,
                        outcome_type=ImportRowOutcomeType.FAILED.value,
                        reason=str(exc) or "Row processing failed",
                        row_summary=row.row_snapshot,
                    )

            import_run = await self.import_trace_service._get_required(import_run_id)
            terminal_status = (
                RunStatus.COMPLETED.value
                if import_run.invalid_row_count == 0
                and import_run.skipped_row_count == 0
                and import_run.failed_row_count == 0
                else RunStatus.COMPLETED_WITH_ERRORS.value
            )
            await self.import_trace_service.complete_import_run(import_run_id, terminal_status)
            import_run = await self.import_trace_service._get_required(import_run_id)
            return _processing_result(import_run)
        except Exception as exc:
            import_run = await self.import_trace_service.complete_import_run(
                import_run_id,
                RunStatus.FAILED.value,
                failure_reason=str(exc),
            )
            return _processing_result(import_run)

    @staticmethod
    def _default_enqueue(
        import_run_id: UUID,
        owner_id: UUID,
        valid_rows: list[dict[str, object]],
        invalid_rows: list[dict[str, object]],
    ) -> object:
        from app.workers.tasks.import_tasks import process_csv_import

        return process_csv_import.delay(str(import_run_id), str(owner_id), valid_rows, invalid_rows)


def _processing_result(import_run) -> ImportProcessingResult:
    return ImportProcessingResult(
        import_run_id=import_run.id,
        status=import_run.status,
        processed_row_count=import_run.processed_row_count,
        inserted_row_count=import_run.inserted_row_count,
        invalid_row_count=import_run.invalid_row_count,
        skipped_row_count=import_run.skipped_row_count,
        failed_row_count=import_run.failed_row_count,
        failure_reason=import_run.failure_reason,
    )
