import asyncio

from common.database import AsyncSessionLocal, SensorData
from common.types import SensorBufferType
from sqlalchemy import insert


async def _dump_queue(buffer: asyncio.Queue[SensorBufferType]):
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
    task = asyncio.create_task(_dump_queue(queue))
    return task
