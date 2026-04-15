from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.notes.models import Note


class NoteRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_active_by_task_id(self, task_id: UUID) -> Note | None:
        result = await self.session.execute(
            select(Note).where(Note.task_id == task_id, Note.deleted_at.is_(None))
        )
        return result.scalar_one_or_none()

    async def add(self, note: Note) -> Note:
        self.session.add(note)
        await self.session.flush()
        return note
