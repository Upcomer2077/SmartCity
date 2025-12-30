import asyncio

from common.database import AsyncSessionLocal, SensorData, engine
from kafka.errors import KafkaTimeoutError, NoBrokersAvailable
from sqlalchemy import select
from sqlalchemy.ext.asyncio.result import AsyncScalarResult

from broker.brokers.kafka_broker import KafkaBroker


async def _get_data():
    async with AsyncSessionLocal() as session:
        result: AsyncScalarResult[SensorData] = await session.stream_scalars(
            select(SensorData)
            .where(SensorData.isDelivered == False)  # noqa: E712
            .limit(limit=20000),
            execution_options={"yield_per": 10000},
        )
        records_ids, records = [], []
        async for i in result:
            records_ids.append(i.id)
            records.append((str(i.sensor_id), i.ts, i.value))
        return records_ids, records


async def launch_broker():
    try:
        kafka_broker = KafkaBroker()
        kafka_broker.bring_me_to_life()

        while True:
            _records_ids, records = await _get_data()
            batch_len = str(len(records))

            if batch_len == 0:
                continue

            print(f"Batch len: {batch_len}")
            kafka_broker.push_to_target("topic", records)

            print(f"Pushed to f{kafka_broker.get_broker_name()}")

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
