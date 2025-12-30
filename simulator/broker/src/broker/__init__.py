import asyncio
import sys

from common.database import AsyncSessionLocal, SensorData, engine
from kafka.errors import NoBrokersAvailable
from sqlalchemy import select
from sqlalchemy.ext.asyncio.result import AsyncScalarResult

from broker.brokers.base_broker import BaseBroker
from broker.brokers.kafka_broker import KafkaBroker


async def get_data():
    async with AsyncSessionLocal() as session:
        result: AsyncScalarResult[SensorData] = await session.stream_scalars(
            select(SensorData).where(SensorData.isDelivered == False),  # noqa: E712
            execution_options={"yield_per": 1000},
        )

        records_ids, records = [], []
        async for i in result:
            records_ids.append(i.id)
            records.append((str(i.sensor_id), i.ts, i.value))

        return records_ids, records


def leave_message_to_broker(broker: BaseBroker, batch):
    broker.push_to_target("topic", batch)
    print("Pushed to Kafka")


async def main():
    try:
        kafka_broker = KafkaBroker()
        kafka_broker.bring_me_to_life()

        while True:
            _records_ids, records = await get_data()

            leave_message_to_broker(kafka_broker, records)
            kafka_broker.broker.flush()

            await asyncio.sleep(10)

    except NoBrokersAvailable as e:
        print(f"✗ Ошибка при создании Kafka producer: {e}")
        sys.exit(1)

    except asyncio.CancelledError:
        print("Interrupted by user (Ctrl+C)")
    except KeyboardInterrupt:
        print("Interrupted by user (Ctrl+C)")
    finally:
        print("👋 Sim stopped")
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
