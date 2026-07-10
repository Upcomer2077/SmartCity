from aiokafka import AIOKafkaProducer

from transmitter.brokers import BaseBroker


class KafkaBroker(BaseBroker):
    """
    Kafka implementation of the BaseBroker.

    Handles connection lifecycle and serialized batch delivery to Kafka topics.
    """

    def __init__(self, btsrp_srvrs: str = "localhost:29092"):
        """
        Set up Kafka connection parameters.

        :param btsrp_srvrs: Address of the Kafka cluster.
        """
        super().__init__()
        self._broker: AIOKafkaProducer
        self._KAFKA_BOOTSTRAP_SERVER = btsrp_srvrs

    async def bring_me_to_life(self):
        """
        Initialize the KafkaProducer with optimized throughput settings.
        Uses Protobuf serialization (SerializeToString) for the payload.
        """
        self._broker = AIOKafkaProducer(
            bootstrap_servers=self._KAFKA_BOOTSTRAP_SERVER,
            acks=1,
            compression_type="gzip",
            max_request_size=1048576 * 5,
            request_timeout_ms=10000,
        )
        await self._broker.start()

    async def push_to_target(self, topic: str, batch):
        """
        Asynchronously send a data batch to a Kafka topic.

        :param topic: Target Kafka topic name.
        :param batch: Protobuf message batch to be serialized and sent.
        """
        await self._broker.send_and_wait(topic, batch)

    def get_broker_name(self) -> str:
        return "Kafka"

    async def stop(self):
        await self._broker.stop()
