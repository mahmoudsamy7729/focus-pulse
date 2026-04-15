from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.modules.notes.repositories.note_repository import NoteRepository
from app.modules.notes.services.note_service import NoteService


def get_note_repository(session: Annotated[AsyncSession, Depends(get_db_session)]) -> NoteRepository:
    return NoteRepository(session)


def get_note_service(repository: Annotated[NoteRepository, Depends(get_note_repository)]) -> NoteService:
    return NoteService(repository)
