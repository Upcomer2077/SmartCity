from contextvars import ContextVar

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from common.database.repos.sqlalchemy import (
    AlchemySensorDataRepository,
    AlchemySensorRepository,
)
from common.database.uow import IUnitOfWork


class AlchemyUnitOfWork(IUnitOfWork):
    """SQLAlchemy implementation of the Unit of Work pattern using context variables."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        """Initialize the UOW with a session factory and a context variable for the session.

        Args:
            session_factory (async_sessionmaker[AsyncSession]): Factory to create async sessions.
        """
        self.session_factory = session_factory
        self._session_var: ContextVar[AsyncSession] = ContextVar("session")

    @property
    def session(self) -> AsyncSession:
        """Get the current active async database session from the context.

        Returns:
            AsyncSession: The current SQLAlchemy async session.
        """
        return self._session_var.get()

    async def __aenter__(self):
        session = self.session_factory()
        self._session_var.set(session)

        self.sensors = AlchemySensorRepository(self.session)
        self.sensor_data = AlchemySensorDataRepository(self.session)
        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await super().__aexit__(exc_type, exc_val, exc_tb)
        await self.session.close()

    async def commit(self):
        """Commit the current database transaction."""
        await self.session.commit()

    async def rollback(self):
        """Roll back the current database transaction."""
        await self.session.rollback()
