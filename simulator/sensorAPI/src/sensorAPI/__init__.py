import asyncio

from common.database import AsyncSessionLocal, Sensor, engine
from common.types import SensorBufferType
from common.types.enums import AvailableSensors
from sqlalchemy import select

from sensorapi.generator import launch_generator
from sensorapi.keeper import start_keeper
from sensorapi.sensors.air_quality.airSensor import AirSensor
from sensorapi.sensors.baseSensor import BaseSensor
from sensorapi.sensors.temperature.temperatureSensor import TemperatureSensor
from sensorapi.sensors.traffic.trafficSensor import TrafficSensor

# Global buffer for cross-task sensor data exchange
shared_queue: asyncio.Queue[SensorBufferType] = asyncio.Queue()


def _get_sensor_type(sensor_type: AvailableSensors):
    """
    Factory mapping for sensor class instantiation.

    :param sensor_type: Enum value representing the sensor category.
    :return: Concrete sensor class reference.
    """
    match sensor_type:
        case AvailableSensors.AIR_Q:
            return AirSensor
        case AvailableSensors.TEMP:
            return TemperatureSensor
        case AvailableSensors.TRAFFIC:
            return TrafficSensor


async def launch_sensors():
    """
    Orchestrator for the sensor simulation ecosystem.

    Loads sensor configuration from DB, initializes concrete sensor objects,
    and runs concurrent generation and persistence tasks.
    """
    try:
        typed_sensors: list[BaseSensor]

        # Fetch sensors from DB with streaming for memory efficiency
        async with AsyncSessionLocal() as session:
            result = await session.stream_scalars(
                select(Sensor), execution_options={"yield_per": 200}
            )

            typed_sensors = [
                _get_sensor_type(sensor.type)(sensor.serial_number, shared_queue)
                async for sensor in result
            ]

        # Fire and forget background workers
        sensor_task = launch_generator(typed_sensors)
        keeper_task = start_keeper(shared_queue)

        # Keep the application running until tasks are canceled
        await asyncio.gather(sensor_task, keeper_task)

    except asyncio.CancelledError, KeyboardInterrupt:
        print("Interrupted by user (Ctrl+C)")

    except Exception as e:
        print(f"❌ Error: {e}")

    # Cleanup database connections and engine resources
    finally:
        try:
            await engine.dispose()
        except Exception:
            print("Cannot dispose engine")
        print("👋 Sensors stopped")


def main():
    """Entry point for the sensor simulation service"""
    print("🚀 Sensors started")
    asyncio.run(launch_sensors())
