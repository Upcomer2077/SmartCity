import asyncio

from sensorAPI.sensors.baseSensor import BaseSensor


async def _start_sensors(sensor_list: list[BaseSensor]):
    print("Generator been started")
    while True:
        start_time = asyncio.get_event_loop().time()

        for s in sensor_list:
            s.tick()

        end_time = asyncio.get_event_loop().time()
        await asyncio.sleep(max(0, 3.0 - (end_time - start_time)))


def launch_generator(sensor_list: list[BaseSensor]):
    return asyncio.create_task(_start_sensors(sensor_list))
