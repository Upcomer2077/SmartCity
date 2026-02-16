from abc import ABC, abstractmethod

from broker.sensor_data_pb2 import SensorBatch


class BaseBroker(ABC):
    """
    Abstract interface for message brokers.
    Defines the contract for pushing data batches to a specific target/topic.
    """

    def __init__(self) -> None:
        super().__init__()
        self._broker = None

    @abstractmethod
    def push_to_target(self, topic: str, batch: SensorBatch):
        """
        Send a data batch to the specified broker topic.

        :param topic: Target destination identifier (topic or queue name).
        :param batch: Data payload to be sent.
        """
        pass

    @abstractmethod
    def get_broker_name(self) -> str:
        """
        Return the human-readable name of the broker implementation.

        :return: Broker implementation name (e.g., 'Kafka', 'RabbitMQ').
        """
        pass
