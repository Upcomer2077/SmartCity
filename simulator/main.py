import asyncio

from aiokafka.errors import KafkaConnectionError, NodeNotReadyError
from common.database.core.sqlite import DBCoreSqlite
from common.database.manager import DBManager
from common.database.uow.sqlalchemy import AlchemyUnitOfWork
from common.logger_ import mlogger
from common.types import SensorBufferType

from collector import launch_collector
from config import DB_URL, KAFKA_BOOTSTRAP_SERVER
from emitter import launch_emitter
from emitter.registry import SensorRegistry
from emitter.utils.get_sensor_type import get_sensor_type
from transmitter import launch_transmitter
from transmitter.brokers.kafka_ import KafkaBroker

# Global buffer for cross-task sensor data exchange
shared_queue: asyncio.Queue[SensorBufferType] = asyncio.Queue()
registry: SensorRegistry


async def main():

    try:
        dbm = DBManager(DBCoreSqlite(DB_URL))
        uow = AlchemyUnitOfWork(dbm.get_session_factory())

        broker = KafkaBroker(KAFKA_BOOTSTRAP_SERVER)
        await broker.bring_me_to_life()
        mlogger.info(f"✓ {broker.get_broker_name()} producer created")

        async with uow:
            result = await uow.sensors.get_all()

            registry = SensorRegistry(
                [
                    get_sensor_type(sensor.type)(sensor.serial_number, shared_queue)
                    for sensor in result
                ]
            )

        async with asyncio.TaskGroup() as tg:
            _emitter = tg.create_task(launch_emitter(registry))
            _collector = tg.create_task(launch_collector(shared_queue, uow))
            _transmitter = tg.create_task(launch_transmitter(broker, uow))

    except asyncio.CancelledError, KeyboardInterrupt:
        mlogger.info("Interrupted by user (Ctrl+C)")

    except KafkaConnectionError as e:
        mlogger.error(f"x Failed to create producer: {e}", e)
    except NodeNotReadyError as e:
        mlogger.error(f"x Timeout error: {e}", e)

    except Exception as e:
        mlogger.error(str(e), e)
    finally:
        try:
            mlogger.info(f"Stopping {broker.get_broker_name()}")
            await asyncio.shield(broker.stop())
            await asyncio.shield(dbm.dispose())
        except Exception as e:
            mlogger.error("Cannot dispose engine", e)
        mlogger.info("👋 Simulator stopped")


if __name__ == "__main__":
    """Entry point for the sensor simulation service"""
    asyncio.run(main())
