import inspect
import logging
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import get_settings


class Base(AsyncAttrs, DeclarativeBase):
    """Shared declarative base for all Phase 1 ORM models."""


settings = get_settings()

engine = create_async_engine(
    settings.database.url,
    echo=settings.database.echo,
    pool_size=settings.database.pool_size,
    max_overflow=settings.database.max_overflow,
)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
logger = logging.getLogger(__name__)


async def _run_after_commit_callbacks(session: AsyncSession) -> None:
    callbacks = list(session.info.pop("after_commit_callbacks", []))
    for callback in callbacks:
        try:
            result = callback()
            if inspect.isawaitable(result):
                await result
        except Exception:  # noqa: BLE001 - callback failures are logged after commit
            logger.exception("post_commit_callback_failed")


async def commit_session(session: AsyncSession) -> None:
    await session.commit()
    await _run_after_commit_callbacks(session)


async def get_db_session() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        session.info.setdefault("after_commit_callbacks", [])
        try:
            yield session
            await commit_session(session)
        except Exception:
            await session.rollback()
            raise
