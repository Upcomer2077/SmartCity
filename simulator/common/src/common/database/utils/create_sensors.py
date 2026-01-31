import asyncio
from random import choice

from common.database import AsyncSessionLocal, Sensor, _Base, engine
from common.types.enums import SensorEnum


async def create_sample_sensors(commit: bool = True) -> list[Sensor]:
    """Create and persist a few sample Sensor rows using SQLAlchemy.

    Returns the list of Sensor instances (detached or persisted depending on session lifecycle).
    """
    async with engine.begin() as conn:
        await conn.run_sync(_Base.metadata.create_all)
    sensors = [
        Sensor(
            type=choice([*SensorEnum]),
            lon=i + 44.222,
            lat=i + 55.222,
        )
        for i in range(0, 100)
    ]

    if commit:
        async with AsyncSessionLocal() as session:
            session.add_all(sensors)
            await session.commit()
    await engine.dispose()
    return sensors


if __name__ == "__main__":
    try:
        created = asyncio.run(create_sample_sensors())
        print(f"Created {len(created)} sensors")
    finally:
        asyncio.run(engine.dispose())
