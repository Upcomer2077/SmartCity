import asyncio

from sensorapi.sensors.registry import SensorRegistry


async def _start_sensors(sensor_registry: SensorRegistry):
    """
    Main simulation loop for sensor data generation.

    Executes a tick for every sensor in the list and attempts
    to maintain a steady 3-second cycle interval.
    """
    print("Generator been started")
    while True:
        start_time = asyncio.get_event_loop().time()

        for s in sensor_registry:
            s.tick()

        end_time = asyncio.get_event_loop().time()
        await asyncio.sleep(max(0, 3.0 - (end_time - start_time)))


def launch_generator(sensor_registry: SensorRegistry):
    """
    Spawns the sensor simulation loop as a background task.

    :param sensor_registry: Registry of initialized sensor instances to simulate.
    :return: Handle to the running generator task.
    """
    return asyncio.create_task(_start_sensors(sensor_registry))
