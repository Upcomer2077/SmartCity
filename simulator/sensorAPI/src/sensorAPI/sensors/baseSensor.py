import asyncio
from abc import ABC, abstractmethod

from common.types import SensorBufferType
from sqlalchemy import UUID


class BaseSensor(ABC):
    __slots__ = ("sensor_sn", "_buffer")

    def __init__(
        self,
        sensor_sn: UUID,
        queue: asyncio.Queue[SensorBufferType],
    ):
        super().__init__()
        self.sensor_sn = sensor_sn
        self._buffer = queue

    @abstractmethod
    def _generate_sensor_data(self) -> SensorBufferType | None:
        raise NotImplementedError("Subclasses must implement method")

    def tick(self) -> None:
        data = self._generate_sensor_data()
        return None if data is None else self._buffer.put_nowait(data)
