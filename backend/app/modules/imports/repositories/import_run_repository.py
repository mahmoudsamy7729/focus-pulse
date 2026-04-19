from uuid import UUID

from sqlalchemy import func, select
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

    async def get(self, import_run_id: UUID, *, include_row_outcomes: bool = False) -> ImportRun | None:
        statement = (
            select(ImportRun)
            .where(ImportRun.id == import_run_id, ImportRun.deleted_at.is_(None))
            .execution_options(populate_existing=True)
        )
        if include_row_outcomes:
            statement = statement.options(selectinload(ImportRun.row_outcomes))
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_owner(self, owner_id: UUID, import_run_id: UUID) -> ImportRun | None:
        result = await self.session.execute(
            select(ImportRun)
            .where(
                ImportRun.id == import_run_id,
                ImportRun.owner_id == owner_id,
                ImportRun.deleted_at.is_(None),
            )
            .execution_options(populate_existing=True)
        )
        return result.scalar_one_or_none()

    async def list_by_owner(self, owner_id: UUID, page: int, limit: int) -> tuple[list[ImportRun], int]:
        total_result = await self.session.execute(
            select(func.count(ImportRun.id)).where(ImportRun.owner_id == owner_id, ImportRun.deleted_at.is_(None))
        )
        result = await self.session.execute(
            select(ImportRun)
            .where(ImportRun.owner_id == owner_id, ImportRun.deleted_at.is_(None))
            .order_by(ImportRun.created_at.desc())
            .offset((page - 1) * limit)
            .limit(limit)
        )
        return list(result.scalars()), int(total_result.scalar_one())

    async def add_row_outcome(self, row_outcome: ImportRowOutcome) -> ImportRowOutcome:
        self.session.add(row_outcome)
        await self.session.flush()
        return row_outcome

    async def list_row_outcomes(
        self,
        owner_id: UUID,
        import_run_id: UUID,
        page: int,
        limit: int,
    ) -> tuple[list[ImportRowOutcome], int]:
        total_result = await self.session.execute(
            select(func.count(ImportRowOutcome.id)).where(
                ImportRowOutcome.owner_id == owner_id,
                ImportRowOutcome.import_run_id == import_run_id,
            )
        )
        result = await self.session.execute(
            select(ImportRowOutcome)
            .where(
                ImportRowOutcome.owner_id == owner_id,
                ImportRowOutcome.import_run_id == import_run_id,
            )
            .order_by(ImportRowOutcome.row_number.asc(), ImportRowOutcome.created_at.asc())
            .offset((page - 1) * limit)
            .limit(limit)
        )
        return list(result.scalars()), int(total_result.scalar_one())
