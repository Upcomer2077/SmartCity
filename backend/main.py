# from asyncio import create_task, run, sleep
import asyncio
import json
from pprint import pprint

from kafka import KafkaConsumer

# engine = create_engine(
#     "postgresql://postgres:pass@localhost:5432/postgres")
# Base.metadata.create_all(bind=engine)

# Session = sessionmaker(bind=engine)
# session = Session()

# consumer = KafkaConsumer('sensors',
#                          group_id='my-group',
#                          bootstrap_servers=['localhost:9092'])
# shutdown_event = asyncio.Event()

# with engine.connect() as connection:
#     try:
#         connection.execute(
#             text("SELECT create_hypertable('sensor_data_hyper', 'time');")
#         )
#         connection.commit()
#         print("Таблица 'sensor_data_hyper' преобразована в гипертаблицу.")
#     except Exception as e:
#         print(e)
#         print("Гипертаблица уже существует.")

consumer = KafkaConsumer("topic", bootstrap_servers=["localhost:9092"])


async def kafka_puller():
    while True:
        try:
            for message in consumer:
                # message value and key are raw bytes -- decode if necessary!
                # e.g., for unicode: `message.value.decode('utf-8')`
                values = json.loads(message.value)
                pprint(values)
                # print(json.loads(message.value))

        except Exception as e:
            print(e)
        await asyncio.sleep(1)


async def main():
    asyncio.create_task(kafka_puller())
    # asyncio.run(tas)
    await asyncio.sleep(1)


if __name__ == "__main__":
    try:
        asyncio.run(kafka_puller())
    except KeyboardInterrupt:
        print("\n\n⚠ Прерывание пользователем (Ctrl+C)")
