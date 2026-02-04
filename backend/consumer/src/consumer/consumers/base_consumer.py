import asyncio
from abc import ABC, abstractmethod

from consumer.sensor_data_pb2 import Global___SensorDTO, SensorBatch
from google.protobuf.internal.containers import RepeatedCompositeFieldContainer


class BaseConsumer(ABC):
    _q: asyncio.Queue[RepeatedCompositeFieldContainer[Global___SensorDTO]]
    _consumer_instance = None
    _Batch: SensorBatch = SensorBatch()

    @abstractmethod
    def __init__(self):
        self._consumer_instance = None
        raise NotImplementedError("Subclasses must implement method")

    @abstractmethod
    def consume(self, message):
        raise NotImplementedError("Subclasses must implement method")

    def _put_batch_to_queue(
        self, batch: RepeatedCompositeFieldContainer[Global___SensorDTO]
    ):
        self._q.put_nowait(batch)

    def get_batch_from_queue(
        self,
    ) -> RepeatedCompositeFieldContainer[Global___SensorDTO]:
        return self._q.get_nowait()

    def is_queue_empty(self) -> bool:
        return self._q.empty()
