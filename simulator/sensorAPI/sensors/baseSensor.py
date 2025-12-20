import asyncio
from abc import ABC, abstractmethod

from common.types import SensorBufferType
from common.types.enums import SensorEnum


class BaseSensor(ABC):
    __slots__ = ("sensor_id", "_buffer")

    def __init__(
        self, sensor_id: str, queue: asyncio.Queue[SensorBufferType], type: SensorEnum
    ):
        self.sensor_id = sensor_id
        self._buffer = queue

    @abstractmethod
    def _generate_sensor_data(self) -> SensorBufferType | None:
        raise NotImplementedError("Subclasses must implement method")

    def tick(self):
        data = self._generate_sensor_data()
        if data is not None:
            return self._buffer.put_nowait(data)
