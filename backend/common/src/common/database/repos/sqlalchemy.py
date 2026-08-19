from common.database import Sensor, SensorData, Sensors
from common.database.repos import ISensorDataRepository, ISensorRepository
from common.database.utils.async_groupby import async_groupby
from ingestor.types import SensorDataBatch
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession


class AlchemySensorRepository(ISensorRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def insert(self, sensor):
        Sensors()
        sensor_upsert_stmt = sensor_upsert_stmt.on_conflict_do_nothing(
            index_elements=["id"]
        )

    async def get_all(self):
        result = await self.session.execute(select(Sensor))

        return result.scalars().all()


class AlchemySensorDataRepository(ISensorDataRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_data(self, data):
        await self.session.execute(
            insert(SensorData),
            data,
        )

    async def get_all(
        self,
        *,
        yield_per: int,
        limit: int | None = None,
    ):
        statement = (
            select(
                SensorData.sensor_sn,
                Sensor.lat,
                Sensor.lon,
                Sensor.type,
                SensorData.ts,
                SensorData.value,
                SensorData.id,
                SensorData.created_at,
            )
            .join(Sensor, Sensor.serial_number == SensorData.sensor_sn)
            .order_by(SensorData.sensor_sn)
            .limit(limit)
        )
        execution_options = {"yield_per": yield_per}

        result = await self.session.stream(
            statement, execution_options=execution_options
        )
        result = result.mappings()
        async for record, group in async_groupby(
            result,
            key_func=lambda row: (
                row["sensor_sn"],
                row["lat"],
                row["lon"],
                row["type"],
            ),
        ):
            yield SensorDataBatch(
                {
                    "sn": str(record[0]),
                    "type": record[3],
                    "lat": record[1],
                    "lon": record[2],
                    "data": [
                        {
                            "ts": g.ts,
                            "value": g.value,
                            "_rowid": g.id,
                            "_created_at": g.created_at,
                        }
                        for g in group
                    ],
                }
            )

    def drop_some(self, *, created_earlier, max_id):
        query = delete(SensorData).where(
            SensorData.created_at <= created_earlier, SensorData.id <= max_id
        )

        return self.session.execute(query)
