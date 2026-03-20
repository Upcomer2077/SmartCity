import asyncio
from abc import ABC, abstractmethod

from consumer.sensor_data_pb2 import SensorBatch, SensorDTO
from google.protobuf.internal.containers import RepeatedCompositeFieldContainer


class BaseConsumer(ABC):
    _q: asyncio.Queue[RepeatedCompositeFieldContainer[SensorDTO]]
    _consumer_instance = None
    _Batch: SensorBatch = SensorBatch()

    @abstractmethod
    def __init__(self):
        self._consumer_instance = None
        raise NotImplementedError("Subclasses must implement method")

    @abstractmethod
    def consume(self, message):
        raise NotImplementedError("Subclasses must implement method")

    def _put_batch_to_queue(self, batch: RepeatedCompositeFieldContainer[SensorDTO]):
        self._q.put_nowait(batch)

    def get_batch_from_queue(
        self,
    ) -> RepeatedCompositeFieldContainer[SensorDTO]:
        return self._q.get_nowait()

    def is_queue_empty(self) -> bool:
        return self._q.empty()
        return self._q.empty()
