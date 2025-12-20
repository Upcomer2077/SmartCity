# """
# SmartCity Sensor Simulator

# Генерирует данные от IoT-датчиков и отправляет их в Kafka.
# Каждый сенсор генерирует данные каждую секунду.
# """

# import json
# import os

# from kafka import KafkaProducer
# from sqlalchemy import select

# from common import AsyncSessionLocal, SensorData

# # load_dotenv()

# KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
# KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "sensors")
# GENERATION_INTERVAL = float(os.getenv("GENERATION_INTERVAL", "1.0"))  # секунды


# async def get_data():
#     while True:
#         async with AsyncSessionLocal() as session:
#             result = await session.stream_scalars(
#                 select(SensorData).where(SensorData.isDelivered == False),  # noqa: E712
#                 execution_options={"yield_per": 200},
#             )

#             batch_ids = []


# def create_kafka_producer() -> KafkaProducer:
#     try:
#         producer = KafkaProducer(
#             bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS.split(","),
#             value_serializer=lambda v: json.dumps(v).encode("utf-8"),
#             acks="all",
#             retries=3,
#             max_in_flight_requests_per_connection=1,
#             compression_type="gzip",
#         )
#         print(f"✓ Kafka producer создан. Сервер: {KAFKA_BOOTSTRAP_SERVERS}")
#         return producer
#     except Exception as e:
#         print(f"✗ Ошибка при создании Kafka producer: {e}")
#         raise
