from contextvars import ContextVar

from common.database.repos.sqlalchemy import (
    AlchemySensorDataRepository,
    AlchemySensorRepository,
)
from common.database.uow import IUnitOfWork
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class AlchemyUnitOfWork(IUnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self.session_factory = session_factory
        self._session_var: ContextVar[AsyncSession] = ContextVar("session")

    @property
    def session(self) -> AsyncSession:
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
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
