from uuid import UUID

from app.modules.notes.exceptions import ActiveNoteExistsError
from app.modules.notes.models import Note
from app.modules.notes.repositories.note_repository import NoteRepository


class NoteService:
    def __init__(self, repository: NoteRepository) -> None:
        self.repository = repository

    async def create_note(
        self,
        owner_id: UUID,
        task_id: UUID,
        content: str | None,
        import_run_id: UUID | None = None,
    ) -> Note | None:
        normalized_content = content.strip() if content is not None else ""
        if not normalized_content:
            return None

        existing = await self.repository.get_active_by_task_id(task_id)
        if existing is not None:
            raise ActiveNoteExistsError("task already has an active note")

        return await self.repository.add(
            Note(owner_id=owner_id, task_id=task_id, content=normalized_content, import_run_id=import_run_id)
        )
