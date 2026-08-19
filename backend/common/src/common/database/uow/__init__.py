from abc import ABC, abstractmethod

from common.database.repos import ISensorDataRepository, ISensorRepository


class IUnitOfWork(ABC):
    sensors: ISensorRepository
    sensor_data: ISensorDataRepository

    @abstractmethod
    async def __aenter__(self):
        """Open a new session, inject it into context, and initialize repositories.

        Returns:
            IUnitOfWork like: The entered context manager instance.
        """
        return self

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Close the active database session upon exiting the context.

        Args:
            exc_type: The exception type if raised, otherwise None.
            exc_val: The exception value if raised, otherwise None.
            exc_tb: The traceback if raised, otherwise None.
        """
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

    @abstractmethod
    async def commit(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass
