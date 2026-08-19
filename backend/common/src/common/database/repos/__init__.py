from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from datetime import datetime

from common.database import SensorDataHyper, Sensors


class ISensorRepository(ABC):
    @abstractmethod
    async def insert(self, one: Sensors): ...


class ISensorDataRepository(ABC):
    @abstractmethod
    async def insert_many(self, l: list[SensorDataHyper]): ...
