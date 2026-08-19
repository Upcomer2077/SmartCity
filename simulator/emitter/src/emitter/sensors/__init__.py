import asyncio
from abc import ABC, abstractmethod
from random import random

from common.types import SensorBufferType
from sqlalchemy import UUID


class BaseSensor(ABC):
    """
    Abstract base class for all simulated sensors.

    Manages common sensor state and asynchronous buffer interaction.
    Uses __slots__ to minimize memory footprint during high-concurrency simulation.
    """

    __slots__ = ("sensor_sn", "_buffer", "is_active")

    def __init__(
        self, sensor_sn: UUID, queue: asyncio.Queue[SensorBufferType], is_active=True
    ):
        """
        Initialize sensor with unique identifier and data destination.

        :param sensor_sn: Unique serial number of the physical sensor.
        :param queue: Async queue to buffer outgoing measurements.
        :param is_active: Shows if sensor in work right now
        """
        super().__init__()
        self.sensor_sn = sensor_sn
        self._buffer = queue
        self.is_active = is_active

    @abstractmethod
    def _emit_data(self) -> SensorBufferType:
        """
        Spams sensor value
        """
        raise NotImplementedError("Not implemented")

    def _generate_sensor_data(self) -> SensorBufferType | None:
        return self._emit_data() if random() > 0.2 else None

    def push_to_buffer(self, data: SensorBufferType):
        self._buffer.put_nowait(data)

    def tick(self):
        """
        Execute a single simulation step.
        Generates data and pushes it to the buffer if available.
        """
        if not self.is_active:
            return False
        data = self._generate_sensor_data()
        if data is None:
            return False

        self.push_to_buffer(data)
        return True
