import asyncio

from common.database import AsyncSessionLocal, Sensor, engine
from common.types import SensorBufferType
from common.types.enums import SensorEnum
from sensorAPI.generator import launch_generator
from sensorAPI.keeper import start_keeper
from sensorAPI.sensors.air_quality.airSensor import AirSensor
from sensorAPI.sensors.baseSensor import BaseSensor
from sensorAPI.sensors.temperature.temperatureSensor import TemperatureSensor
from sensorAPI.sensors.traffic.trafficSensor import TrafficSensor
from sqlalchemy import select

shared_queue: asyncio.Queue[SensorBufferType] = asyncio.Queue()


def get_sensor_type(sensor_type: SensorEnum):
    match sensor_type:
        case SensorEnum.AIR_Q:
            return AirSensor
        case SensorEnum.TEMP:
            return TemperatureSensor
        case SensorEnum.TRAFFIC:
            return TrafficSensor


async def main():
    try:
        typed_sensors: list[BaseSensor]

        async with AsyncSessionLocal() as session:
            result = await session.stream_scalars(
                select(Sensor), execution_options={"yield_per": 200}
            )

            typed_sensors = [
                get_sensor_type(sensor.type)(sensor.sensor_id, shared_queue)
                async for sensor in result
            ]

        sensor_task = launch_generator(typed_sensors)
        keeper_task = start_keeper(shared_queue)

        await asyncio.gather(sensor_task, keeper_task)
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        print("👋 Sim stopped")
        asyncio.run(engine.dispose())


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("⚠ Interrupted by user (Ctrl+C)")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    print("👋 Sim stopped")
    asyncio.run(engine.dispose())
