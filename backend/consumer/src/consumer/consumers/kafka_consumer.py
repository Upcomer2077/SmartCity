from consumer.consumers.base_consumer import BaseConsumer
from kafka import KafkaConsumer as KfkConsumer


class KafkaConsumer(BaseConsumer):
    def __init__(self, topic: str, bootstrap_servers: list[str]):
        self._consumer_instance: KfkConsumer = KfkConsumer(
            topic, bootstrap_servers=bootstrap_servers
        )

    def get_consumer_instance(self):
        return self._consumer_instance

    def consume(self, message):
        self._Batch.ParseFromString(serialized=message.value)
        self._put_batch_to_queue(batch=self._Batch.records)
