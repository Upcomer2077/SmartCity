import asyncio
from common.logger_ import mlogger
from common.database.uow import IUnitOfWork
from common.types import SensorBufferType


async def _dump_queue(buffer: asyncio.Queue[SensorBufferType], uow: IUnitOfWork):
    """
    Background worker to persist buffered sensor data.

    Periodically flushes the async queue to the database using bulk inserts.
    Runs in an infinite loop with a 10-second interval by default.
    """
    mlogger.info("Collector has been started")
    while True:
        await asyncio.sleep(10)
        batch: list[SensorBufferType] = []

        while not buffer.empty():
            batch.append(buffer.get_nowait())
            buffer.task_done()

        if not batch:
            continue

        async with uow:
            await uow.sensor_data.add_data(batch)
        mlogger.info(f"Data-batch with l({len(batch)}) has been pushed to database")


# TODO: add flush timeout param
async def launch_collector(queue: asyncio.Queue[SensorBufferType], uow: IUnitOfWork):
    """
    Initialize and run the data persistence worker.

    :param queue: Async queue containing sensor measurements.
    :return: Non-blocking asyncio Task object.
    """
    return await _dump_queue(queue, uow)
