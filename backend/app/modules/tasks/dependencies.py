from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.modules.notes.dependencies import get_note_service
from app.modules.notes.services.note_service import NoteService
from app.modules.tasks.repositories.task_repository import CategoryRepository, TaskRepository
from app.modules.tasks.services.task_service import TaskService


def get_task_repository(session: Annotated[AsyncSession, Depends(get_db_session)]) -> TaskRepository:
    return TaskRepository(session)


def get_category_repository(session: Annotated[AsyncSession, Depends(get_db_session)]) -> CategoryRepository:
    return CategoryRepository(session)


def get_task_service(
    task_repository: Annotated[TaskRepository, Depends(get_task_repository)],
    category_repository: Annotated[CategoryRepository, Depends(get_category_repository)],
    note_service: Annotated[NoteService, Depends(get_note_service)],
) -> TaskService:
    return TaskService(task_repository, category_repository, note_service)
