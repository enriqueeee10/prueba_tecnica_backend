from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from contextlib import asynccontextmanager
from app.shared.infrastructure.base import Base


class Database:
    def __init__(self, database_url: str):
        # Convert sync URL to async URL for PostgreSQL
        if database_url.startswith("postgresql://"):
            database_url = database_url.replace(
                "postgresql://", "postgresql+asyncpg://"
            )

        self.engine = create_async_engine(database_url, echo=True)
        self._session_factory = async_sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

    @property
    def session(self):
        """Return the session factory for dependency injection"""
        return self._session_factory

    def get_session(self):
        """Get the session factory for dependency injection"""
        return self._session_factory

    @asynccontextmanager
    async def session_context(self):
        """Provide a transactional scope around a series of operations."""
        async with self._session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


__all__ = ["Database", "Base"]
