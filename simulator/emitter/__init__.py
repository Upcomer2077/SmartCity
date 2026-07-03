from emitter.generator import start_sensors
from emitter.registry import SensorRegistry


async def launch_emitter(registry: SensorRegistry):
    return await start_sensors(registry)
