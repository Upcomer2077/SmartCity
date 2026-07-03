import asyncio

from common.logger_ import mlogger

from emitter.registry import SensorRegistry


async def start_sensors(sensor_registry: SensorRegistry):
    """
    Main simulation loop for sensor data generation.

    Executes a tick for every sensor in the list and attempts
    to maintain a steady 3-second cycle interval.
    """
    mlogger.info("Emitter has been started")
    while True:
        ticks = 0
        start_time = asyncio.get_event_loop().time()

        for s in sensor_registry:
            tick = s.tick()
            ticks += 1 if tick else 0

        end_time = asyncio.get_event_loop().time()
        mlogger.info(f"{ticks} sensors ticked")
        await asyncio.sleep(max(0, 3.0 - (end_time - start_time)))
