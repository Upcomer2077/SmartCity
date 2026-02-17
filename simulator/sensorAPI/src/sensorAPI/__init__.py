import asyncio

from common.database import AsyncSessionLocal, Sensor, engine
from common.types import SensorBufferType
from sqlalchemy import select

from sensorapi.generator import launch_generator
from sensorapi.keeper import start_keeper
from sensorapi.sensors.registry import SensorRegistry
from sensorapi.utils.get_sensor_type import get_sensor_type

# Global buffer for cross-task sensor data exchange
shared_queue: asyncio.Queue[SensorBufferType] = asyncio.Queue()
registry: SensorRegistry


async def launch_sensors():
    """
    Orchestrator for the sensor simulation ecosystem.

    Loads sensor configuration from DB, initializes concrete sensor objects,
    and runs concurrent generation and persistence tasks.
    """
    try:
        # Fetch sensors from DB with streaming for memory efficiency
        async with AsyncSessionLocal() as session:
            result = await session.stream_scalars(
                select(Sensor), execution_options={"yield_per": 200}
            )

            registry = SensorRegistry(
                [
                    get_sensor_type(sensor.type)(sensor.serial_number, shared_queue)
                    async for sensor in result
                ]
            )

        # Fire and forget background workers
        sensor_task = launch_generator(registry)
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
