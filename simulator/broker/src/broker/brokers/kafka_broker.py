import json
import os
from broker.brokers.base_broker import BaseBroker
from kafka import KafkaProducer


class KafkaBroker(BaseBroker):
    def __init__(self):
        super().__init__()
        self.broker: KafkaProducer
        self.KAFKA_BOOTSTRAP_SERVERS = os.getenv(
            "KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"
        )
        self.KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "sensors")

    def bring_me_to_life(self):
        self.broker = KafkaProducer(
            bootstrap_servers="localhost:9092",
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            acks="all",
            retries=3,
            max_in_flight_requests_per_connection=1,
            compression_type="gzip",
        )
        print(f"✓ Kafka producer создан. Сервер: {self.KAFKA_BOOTSTRAP_SERVERS}")

    def push_to_target(self, topic: str, batch: list[str]):
        self.broker.send(topic, value=batch)
