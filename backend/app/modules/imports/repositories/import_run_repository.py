from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.imports.models import ImportRowOutcome, ImportRun


class ImportRunRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, import_run: ImportRun) -> ImportRun:
        self.session.add(import_run)
        await self.session.flush()
        return import_run

    async def get(self, import_run_id: UUID) -> ImportRun | None:
        result = await self.session.execute(
            select(ImportRun)
            .where(ImportRun.id == import_run_id, ImportRun.deleted_at.is_(None))
            .options(selectinload(ImportRun.row_outcomes))
            .execution_options(populate_existing=True)
        )
        return result.scalar_one_or_none()

    async def add_row_outcome(self, row_outcome: ImportRowOutcome) -> ImportRowOutcome:
        self.session.add(row_outcome)
        await self.session.flush()
        return row_outcome
