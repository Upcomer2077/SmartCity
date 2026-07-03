from abc import ABC, abstractmethod

from common.database.repos import ISensorDataRepository, ISensorRepository


class IUnitOfWork(ABC):
    sensors: ISensorRepository
    sensor_data: ISensorDataRepository

    @abstractmethod
    async def __aenter__(self):
        return self

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
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
