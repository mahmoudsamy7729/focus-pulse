from uuid import UUID

from app.core.database import AsyncSessionLocal
from app.modules.daily_logs.repositories.daily_log_repository import DailyLogRepository
from app.modules.daily_logs.services.daily_log_service import DailyLogService
from app.modules.imports.repositories.import_run_repository import ImportRunRepository
from app.modules.imports.schemas import InvalidImportRow, NormalizedImportRow
from app.modules.imports.services.csv_import_service import CSVImportService
from app.modules.imports.services.csv_parser_service import CSVParserService
from app.modules.imports.services.import_trace_service import ImportTraceService
from app.modules.notes.repositories.note_repository import NoteRepository
from app.modules.notes.services.note_service import NoteService
from app.modules.tasks.repositories.task_repository import CategoryRepository, TaskRepository
from app.modules.tasks.services.task_service import TaskService
from app.workers.asyncio_runner import run_async
from app.workers.celery_app import celery_app


async def process_csv_import_payload(
    import_run_id: UUID,
    owner_id: UUID,
    valid_rows: list[dict[str, object]],
    invalid_rows: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    async with AsyncSessionLocal() as session:
        trace_service = ImportTraceService(ImportRunRepository(session))
        service = CSVImportService(
            CSVParserService(),
            trace_service,
            DailyLogService(DailyLogRepository(session)),
            TaskService(
                TaskRepository(session),
                CategoryRepository(session),
                NoteService(NoteRepository(session)),
                import_trace_service=trace_service,
            ),
        )
        result = await service.process_import_payload(
            import_run_id=import_run_id,
            owner_id=owner_id,
            valid_rows=[NormalizedImportRow.model_validate(row) for row in valid_rows],
            invalid_rows=[InvalidImportRow.model_validate(row) for row in invalid_rows or []],
        )
        await session.commit()
        return result.model_dump(mode="json")


if celery_app is not None:

    @celery_app.task(name="imports.process_csv_import")
    def process_csv_import(
        import_run_id: str,
        owner_id: str,
        valid_rows: list[dict[str, object]],
        invalid_rows: list[dict[str, object]] | None = None,
    ) -> dict[str, object]:
        return run_async(
            process_csv_import_payload(
                UUID(import_run_id),
                UUID(owner_id),
                valid_rows,
                invalid_rows,
            )
        )

else:

    class _ProcessCSVImportFallback:
        def delay(
            self,
            import_run_id: str,
            owner_id: str,
            valid_rows: list[dict[str, object]],
            invalid_rows: list[dict[str, object]] | None = None,
        ) -> dict[str, object]:
            return {
                "queued": False,
                "import_run_id": import_run_id,
                "owner_id": owner_id,
                "valid_row_count": len(valid_rows),
                "invalid_row_count": len(invalid_rows or []),
            }

    process_csv_import = _ProcessCSVImportFallback()
