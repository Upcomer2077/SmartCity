from abc import ABC, abstractmethod
from datetime import datetime
from typing import AsyncGenerator

from common.database import Sensor
from common.types import SensorBufferType, SensorDataBatch


class ISensorRepository(ABC):
    @abstractmethod
    async def add(self, sensor): ...

    @abstractmethod
    async def add_list(self, sensors: list[Sensor]): ...

    @abstractmethod
    async def get(self, sensor_id) -> list[Sensor]: ...

    @abstractmethod
    async def get_all(self) -> list[Sensor]: ...


class ISensorDataRepository(ABC):
    @abstractmethod
    async def add_data(self, data: list[SensorBufferType]) -> None: ...

    @abstractmethod
    def get_all(
        self, *, limit: int | None = None, yield_per: int
    ) -> AsyncGenerator[SensorDataBatch]: ...

    @abstractmethod
    async def drop_some(self, *, created_earlier: float | datetime, max_id: int): ...
