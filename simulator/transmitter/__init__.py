import asyncio
from datetime import datetime

from common.database.uow import IUnitOfWork
from common.logger_ import mlogger

from config import BROKER_TOPIC
from transmitter.brokers import BaseBroker
from transmitter.schema.proto import sensor_data_pb2


async def _get_data(uow: IUnitOfWork):
    """
    Fetch undelivered sensor data from the database.

    Streams up to 20,000 records and converts them into a Protobuf SensorBatch.

    :return: A tuple containing a list of record IDs and the Protobuf batch object.
    """
    async with uow:
        data_stream = uow.sensor_data.get_all(yield_per=10000)
        payload = sensor_data_pb2.BulkIngestionPayload()
        max_id = 0
        max_ts = datetime.min
        total_rows = 0
        async for i in data_stream:
            device_data_batch = payload.batches.add()

            device_data_batch.sensor_sn = i["sn"]
            device_data_batch.type = i["type"].value
            device_data_batch.lat = i["lat"]
            device_data_batch.lon = i["lon"]

            for point in i["data"]:
                telemetry_point = device_data_batch.data.add()
                telemetry_point.ts = point["ts"]
                telemetry_point.value = point["value"]
                max_id = max(point["_rowid"], max_id)
                max_ts = max(point["_created_at"], max_ts)
                total_rows += 1

        return max_id, max_ts, total_rows, payload


async def start_broker(broker: BaseBroker, uow: IUnitOfWork):
    """
    Main broker loop to bridge database and Kafka.

    Initializes the Kafka producer and periodically pushes undelivered
    batches to the specified topic.
    """
    mlogger.info("Transmitter has been launched")
    while True:
        max_id, max_ts, total_rows, payload = await _get_data(uow)

        batch_len = len(payload.batches)

        if batch_len > 0:
            await broker.push_to_target(BROKER_TOPIC, payload.SerializeToString())

            mlogger.info(
                f"Batch with {batch_len} sensors ({total_rows} records) has been pushed to {broker.get_broker_name()}"
            )
            async with uow:
                await uow.sensor_data.drop_some(max_id=max_id, created_earlier=max_ts)

        await asyncio.sleep(10)


async def launch_transmitter(broker: BaseBroker, uow: IUnitOfWork):
    """Service entry point for the broker worker."""
    return await start_broker(broker, uow)
