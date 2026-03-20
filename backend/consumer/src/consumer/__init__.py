import sys

from consumer.sensor_data_pb2 import SensorBatch
from kafka import KafkaConsumer


consumer = KafkaConsumer("topic", bootstrap_servers=["localhost:29092"])


def kafka_puller():
    print("puller")
    i = 0
    batch: SensorBatch = SensorBatch()
    try:
        for message in consumer:
            # Десериализуем protobuf сообщение
            batch.ParseFromString(message.value)

            # Выводим каждое сообщение в батче
            # for record in batch.records:
            #     print(
            #         f"  Sensor ID: {record.sensor_id}, Value: {record.value}, Timestamp: {record.ts}"
            #     )
            print(batch.records[0])
            # sensor = session.query(
            #     Sensors).filter_by(sensor_id=values['sensor_id']).first()
            # # print(sensor)
            # if sensor:
            #     # session.add(SensorDataHyper(
            #     #     sensor_id=values['sensor_id'], data=values['value'], time=values['timestamp']))
            #     insert(SensorDataHyper).values(sensor_id=values['sensor_id'], data=values['value'], time=values['timestamp']).on_conflict_do_nothing(
            #         index_elements=["id"])
            #     session.commit()
            print(f"Iteration {i}, batch len: {len(batch.records)}")
            i += 1
            batch.Clear()
    except Exception as e:
        print(e)
        # session.rollback()


def main() -> None:
    print("Hello from consumer!")
    # asyncio.run(kafka_puller())
    try:
        kafka_puller()
    except KeyboardInterrupt:
        print("Keyboard Interrupt. Stopping consumer...")
    except Exception as e:
        print(e)
        print("Error. Stopping consumer...")
        sys.exit(1)
