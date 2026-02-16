import asyncio
import os

from common.database import AsyncSessionLocal, SensorData, engine
from kafka.errors import KafkaTimeoutError, NoBrokersAvailable
from sqlalchemy import select
from sqlalchemy.ext.asyncio.result import AsyncScalarResult

from broker import sensor_data_pb2
from broker.brokers.kafka_broker import KafkaBroker


async def _get_data():
    async with AsyncSessionLocal() as session:
        result: AsyncScalarResult[SensorData] = await session.stream_scalars(
            select(SensorData)
            .where(SensorData.is_delivered == False)  # noqa: E712 !Do not disturb
            .limit(limit=20000),
            execution_options={"yield_per": 10000},
        )
        records_ids: list[int] = []
        batch = sensor_data_pb2.SensorBatch()

        async for i in result:
            records_ids.append(i.id)
            sensor_item = batch.records.add()
            sensor_item.ts = i.ts.timestamp()
            sensor_item.sensor_sn = str(i.sensor_sn)
            sensor_item.value = i.value
        return records_ids, batch


async def launch_broker():
    print("Broker been launched")
    try:
        bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        kafka_broker = KafkaBroker(bootstrap_servers)
        kafka_broker.bring_me_to_life()

        while True:
            _records_ids, batch = await _get_data()
            batch_len = str(len(batch.records))

            if batch_len == 0:
                continue

            print(f"Batch len: {batch_len}")
            kafka_broker.push_to_target("topic", batch)

            print(f"Pushed to {kafka_broker.get_broker_name()}")

            # TODO: update in db
            await asyncio.sleep(10)

    except NoBrokersAvailable as e:
        print(f"✗ Ошибка при создании Kafka producer: {e}")

    except KafkaTimeoutError as e:
        print("Failed to update metadata after 60.0 secs.", e)

    except asyncio.CancelledError, KeyboardInterrupt:
        print("Interrupted by user (Ctrl+C)")

    finally:
        try:
            await engine.dispose()
        except Exception:
            print("Cannot dispose engine")
        print("👋 Broker stopped")


def main():
    asyncio.run(launch_broker())
