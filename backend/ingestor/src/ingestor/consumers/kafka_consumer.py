from aiokafka import AIOKafkaConsumer

from ingestor.consumers import BaseConsumer


class KafkaConsumer(BaseConsumer):
    def __init__(self, topic: str, bootstrap_servers: str):
        self._consumer = AIOKafkaConsumer(topic, bootstrap_servers=bootstrap_servers)
        super().__init__()

    def __aiter__(self):
        return self._consumer.__aiter__()

    def __anext__(self):
        return self._consumer.__anext__()

    async def start(self):
        await self._consumer.start()

    async def stop(self):
        await self._consumer.stop()
