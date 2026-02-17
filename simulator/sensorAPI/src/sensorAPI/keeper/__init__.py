import asyncio

from common import DBManager
from common.database import SensorData
from common.types import SensorBufferType
from sqlalchemy import insert


async def _dump_queue(buffer: asyncio.Queue[SensorBufferType]):
    """
    Background worker to persist buffered sensor data.

    Periodically flushes the async queue to the database using bulk inserts.
    Runs in an infinite loop with a 10-second interval by default.
    """
    print("Keeper been started")
    while True:
        await asyncio.sleep(10)
        batch: list[SensorBufferType] = []

        while not buffer.empty():
            batch.append(buffer.get_nowait())
            buffer.task_done()

        if not batch:
            continue

        async with DBManager.ASYNC_SESSION_LOCAL() as session:
            async with session.begin():
                await session.execute(
                    insert(SensorData),
                    batch,
                )
        print(f"Data-batch with l({len(batch)}) been pushed to db")


# TODO: add flush timeout param
def start_keeper(queue: asyncio.Queue[SensorBufferType]):
    """
    Initialize and run the data persistence worker.

    :param queue: Async queue containing sensor measurements.
    :return: Non-blocking asyncio Task object.
    """
    return asyncio.create_task(_dump_queue(queue))
