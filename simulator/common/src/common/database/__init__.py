import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Enum,
    ForeignKey,
    Index,
    Integer,
    Text,
    event,
)
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql.functions import now
from sqlalchemy.types import UUID, Float, Uuid

from common.types.enums import SensorEnum


class _Base(DeclarativeBase):
    pass


class Sensor(_Base):
    __tablename__ = "sensor"

    sensor_id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    lat: Mapped[float] = mapped_column(Float, nullable=False)
    lon: Mapped[float] = mapped_column(Float, nullable=False)
    type: Mapped[SensorEnum] = mapped_column(Enum(SensorEnum), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=now())

    __table_args__ = (Index("idx_sensor_lat_lon", "lat", "lon", "type", unique=True),)


class SensorData(_Base):
    __tablename__ = "sensor_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ts: Mapped[float] = mapped_column(Float, nullable=False)
    sensor_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("sensor.sensor_id"), nullable=False
    )
    value: Mapped[str] = mapped_column(Text, nullable=False)
    isDelivered: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    __table_args__ = (
        Index("idx_sensordata_sensor_ts", "sensor_id", "ts", unique=True),
        Index("idx_delivery_queue", "id", sqlite_where=(isDelivered == 0)),
    )


DATABASE_URL = "sqlite+aiosqlite:///./db.db"

engine = create_async_engine(
    DATABASE_URL, echo=False, pool_pre_ping=True, connect_args={"timeout": 30}
)


@event.listens_for(engine.sync_engine, "connect")
def set_sqlite_pragma(dbapi_connection, _connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.execute("PRAGMA cache_size=-20000")
    cursor.execute("PRAGMA busy_timeout=30000")
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
