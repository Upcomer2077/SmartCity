from broker.brokers.base_broker import BaseBroker
from kafka import KafkaProducer


class KafkaBroker(BaseBroker):
    def __init__(self, btsrp_srvrs: str | list[str] = "localhost:9092"):
        super().__init__()
        self._broker: KafkaProducer
        self._KAFKA_BOOTSTRAP_SERVERS = btsrp_srvrs

    def bring_me_to_life(self):
        self._broker = KafkaProducer(
            bootstrap_servers=self._KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: v.SerializeToString(),
            acks=1,
            retries=3,
            max_in_flight_requests_per_connection=1,
            compression_type="gzip",
            max_request_size=2e6,
        )
        print(f"✓ Kafka producer создан. Сервер(ы): {self._KAFKA_BOOTSTRAP_SERVERS}")

    def push_to_target(self, topic: str, batch):
        self._broker.send(topic, value=batch)

    def get_broker_name(self) -> str:
        return "Kafka"
