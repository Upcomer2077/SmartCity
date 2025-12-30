import asyncio

from common.database import AsyncSessionLocal, Sensor, engine
from common.types import SensorBufferType
from common.types.enums import SensorEnum
from sqlalchemy import select

from sensorAPI.generator import launch_generator
from sensorAPI.keeper import start_keeper
from sensorAPI.sensors.air_quality.airSensor import AirSensor
from sensorAPI.sensors.baseSensor import BaseSensor
from sensorAPI.sensors.temperature.temperatureSensor import TemperatureSensor
from sensorAPI.sensors.traffic.trafficSensor import TrafficSensor

shared_queue: asyncio.Queue[SensorBufferType] = asyncio.Queue()


def _get_sensor_type(sensor_type: SensorEnum):
    match sensor_type:
        case SensorEnum.AIR_Q:
            return AirSensor
        case SensorEnum.TEMP:
            return TemperatureSensor
        case SensorEnum.TRAFFIC:
            return TrafficSensor


async def launch_sensors():
    try:
        typed_sensors: list[BaseSensor]

        async with AsyncSessionLocal() as session:
            result = await session.stream_scalars(
                select(Sensor), execution_options={"yield_per": 200}
            )

            typed_sensors = [
                _get_sensor_type(sensor.type)(sensor.sensor_id, shared_queue)
                async for sensor in result
            ]

        sensor_task = launch_generator(typed_sensors)
        keeper_task = start_keeper(shared_queue)

        await asyncio.gather(sensor_task, keeper_task)

    except asyncio.CancelledError, KeyboardInterrupt:
        print("Interrupted by user (Ctrl+C)")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        try:
            await engine.dispose()
        except Exception:
            print("Cannot dispose engine")
        print("👋 Sensors stopped")


def main():
    asyncio.run(launch_sensors())
