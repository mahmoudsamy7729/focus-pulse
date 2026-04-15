from datetime import date
from typing import Protocol
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.daily_logs.models import DailyLog
from app.modules.notes.services.note_service import NoteService
from app.modules.tasks.exceptions import InvalidTaskError
from app.modules.tasks.models import Category, Task
from app.modules.tasks.repositories.task_repository import CategoryRepository, TaskRepository
from app.shared.enums.source import SourceLabel, normalize_text


class ImportTraceRecorder(Protocol):
    async def record_import_row_outcome(
        self,
        import_run_id: UUID,
        row_number: int | None,
        outcome_type: str,
        reason: str,
        row_summary: dict[str, object] | None = None,
    ) -> object:
        ...


class TaskService:
    def __init__(
        self,
        task_repository: TaskRepository,
        category_repository: CategoryRepository,
        note_service: NoteService | None = None,
        import_trace_service: ImportTraceRecorder | None = None,
    ) -> None:
        self.task_repository = task_repository
        self.category_repository = category_repository
        self.note_service = note_service
        self.import_trace_service = import_trace_service

    @staticmethod
    def normalize_tags(tags: list[str] | None) -> list[str]:
        normalized: list[str] = []
        seen: set[str] = set()
        for tag in tags or []:
            value = normalize_text(tag)
            if value and value not in seen:
                normalized.append(value)
                seen.add(value)
        return normalized

    async def get_or_create_category(self, owner_id: UUID, category_name: str) -> Category:
        normalized_name = normalize_text(category_name)
        if not normalized_name:
            raise InvalidTaskError("category_name must not be empty")

        existing = await self.category_repository.get_by_normalized_name(owner_id, normalized_name)
        if existing is not None:
            return existing

        canonical_name = " ".join(category_name.strip().split())
        return await self.category_repository.add(
            Category(owner_id=owner_id, name=canonical_name, normalized_name=normalized_name)
        )

    async def create_task(
        self,
        owner_id: UUID,
        daily_log: DailyLog,
        title: str,
        time_spent_minutes: int,
        category_name: str,
        tags: list[str] | None = None,
        note: str | None = None,
        import_run_id: UUID | None = None,
        row_number: int | None = None,
        row_snapshot: dict[str, object] | None = None,
    ) -> Task:
        normalized_title = normalize_text(title)
        if not normalized_title:
            raise InvalidTaskError("title must not be empty")
        if time_spent_minutes <= 0:
            raise InvalidTaskError("time_spent_minutes must be positive")

        if import_run_id is not None:
            duplicate = await self.task_repository.get_import_duplicate(
                owner_id,
                daily_log.log_date,
                normalized_title,
                time_spent_minutes,
            )
            if duplicate is not None:
                if self.import_trace_service is not None:
                    await self.import_trace_service.record_import_row_outcome(
                        import_run_id=import_run_id,
                        row_number=row_number,
                        outcome_type="skipped",
                        reason="Duplicate imported task",
                        row_summary=row_snapshot
                        or {
                            "normalized_task_name": normalized_title,
                            "log_date": daily_log.log_date.isoformat(),
                            "time_spent_minutes": time_spent_minutes,
                        },
                    )
                return duplicate

        category = await self.get_or_create_category(owner_id, category_name)
        task = await self.task_repository.add(
            Task(
                owner_id=owner_id,
                daily_log_id=daily_log.id,
                category_id=category.id,
                title=" ".join(title.strip().split()),
                normalized_title=normalized_title,
                time_spent_minutes=time_spent_minutes,
                tags=self.normalize_tags(tags),
                source=SourceLabel.CSV_IMPORT.value if import_run_id else SourceLabel.MANUAL.value,
                import_run_id=import_run_id,
            )
        )

        if self.note_service is not None:
            await self.note_service.create_note(
                owner_id=owner_id,
                task_id=task.id,
                content=note,
                import_run_id=import_run_id,
            )
        return task

    async def calculate_totals(self, owner_id: UUID, start_date: date, end_date: date) -> dict[str, object]:
        if start_date > end_date:
            raise InvalidTaskError("start_date must be on or before end_date")
        return await self.task_repository.calculate_totals(owner_id, start_date, end_date)


def build_task_service(session: AsyncSession) -> TaskService:
    from app.modules.notes.repositories.note_repository import NoteRepository

    return TaskService(
        task_repository=TaskRepository(session),
        category_repository=CategoryRepository(session),
        note_service=NoteService(NoteRepository(session)),
    )
