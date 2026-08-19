import asyncio
import sys

from ingestor.consumers import BaseConsumer
from ingestor.consumers.kafka_consumer import KafkaConsumer
from ingestor.parser import ProtoParser


async def push_to_database(): ...
async def consume(consumer: BaseConsumer):
    proto_p = ProtoParser()

    async for msg in consumer:
        if not msg.value:
            continue
        yield proto_p.get_data_from_bytes(msg.value)


async def ingestor():
    try:
        consumer: BaseConsumer = KafkaConsumer("telemetry", "localhost:29092")
        await consumer.start()
        async for result in consume(consumer):
            print(result[0])
            await push_to_database()

    except Exception as e:
        print(e)
    finally:
        await consumer.stop()


def main() -> None:
    try:
        print("Hello from consumer!")
        asyncio.run(ingestor())
    except KeyboardInterrupt:
        print("Keyboard Interrupt. Stopping consumer...")
    except Exception as e:
        print(e)
        print("Error. Stopping ingestor...")
        sys.exit(1)
