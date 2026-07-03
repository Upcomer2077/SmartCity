import asyncio
from os import getenv
from random import choice

from common.database import Sensor
from common.database.core.sqlite import DBCoreSqlite
from common.database.manager import DBManager
from common.database.uow.sqlalchemy import AlchemyUnitOfWork
from common.types.enums import AvailableSensors
from dotenv import load_dotenv

load_dotenv()
dbm = DBManager(DBCoreSqlite(getenv("DB_URL") or ""))
uow = AlchemyUnitOfWork(dbm.get_session_factory())


async def create_sample_sensors(commit: bool = True) -> list[Sensor]:
    """Create and persist a few sample Sensor rows using SQLAlchemy.

    Returns the list of Sensor instances (detached or persisted depending on session lifecycle).
    """
    sensors = [
        Sensor(
            type=choice([*AvailableSensors]),
            lon=i + 44.222,
            lat=i + 55.222,
        )
        for i in range(10000)
    ]
    if commit:
        async with uow:
            await uow.sensors.add_list(sensors)
    return sensors


if __name__ == "__main__":
    try:
        created = asyncio.run(create_sample_sensors())
        print(f"Created {len(created)} sensors")
    finally:
        asyncio.run(dbm.dispose())
