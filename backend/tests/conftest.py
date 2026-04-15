import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.database import Base

from app.modules.ai_insights import models as ai_insight_models  # noqa: F401
from app.modules.daily_logs import models as daily_log_models  # noqa: F401
from app.modules.imports import models as import_models  # noqa: F401
from app.modules.notes import models as note_models  # noqa: F401
from app.modules.tasks import models as task_models  # noqa: F401


@pytest_asyncio.fixture
async def async_session() -> AsyncSession:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        yield session

    await engine.dispose()
