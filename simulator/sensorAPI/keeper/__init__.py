import asyncio

from sqlalchemy import insert

from common.database import AsyncSessionLocal, SensorData
from common.types import SensorBufferType


async def dump_queue(buffer: asyncio.Queue[SensorBufferType]):
    while True:
        await asyncio.sleep(10)
        batch: list[SensorBufferType] = []

        while not buffer.empty():
            batch.append(buffer.get_nowait())
            buffer.task_done()

        if not batch:
            continue

        async with AsyncSessionLocal() as session:
            async with session.begin():
                await session.execute(
                    insert(SensorData),
                    batch,
                )


def start_keeper(queue: asyncio.Queue[SensorBufferType]):
    task = asyncio.create_task(dump_queue(queue))
    return task
