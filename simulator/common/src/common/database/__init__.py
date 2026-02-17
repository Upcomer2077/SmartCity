import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Enum,
    ForeignKey,
    Index,
    Integer,
    event,
)
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm.properties import MappedColumn
from sqlalchemy.sql.functions import now
from sqlalchemy.types import UUID, Float, Uuid

from common.types.enums import AvailableSensors


class _Base(DeclarativeBase):
    pass


class Sensor(_Base):
    """
    Registry for physical sensors.
    Stores location, type, and operational status.
    """

    __tablename__ = "sensors"

    serial_number: Mapped[UUID] = mapped_column(
        Uuid, primary_key=True, default=uuid.uuid4
    )
    lat: Mapped[float] = mapped_column(Float, nullable=False)
    lon: Mapped[float] = mapped_column(Float, nullable=False)
    type: Mapped[AvailableSensors] = mapped_column(
        Enum(AvailableSensors), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=now())

    __table_args__ = (Index("idx_sensors_lat_lon", "lat", "lon", "type", unique=True),)


class SensorData(_Base):
    """
    Time-series storage for sensor measurements.
    Maps to SQLite rowid for primary key efficiency.
    """

    __tablename__ = "sensor_data"
    id: MappedColumn[int] = mapped_column(Integer, name="rowid", primary_key=True)
    ts: Mapped[datetime] = mapped_column(Float, nullable=False)
    sensor_sn: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("sensors.serial_number", ondelete="CASCADE", name="fkssn"),
        nullable=False,
    )
    value: Mapped[float] = mapped_column(Float, nullable=False)
    is_delivered: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    __table_args__ = (
        Index("idx_sensordata_sensor_ts", "sensor_sn", "ts", unique=True),
    )


DATABASE_URL = "sqlite+aiosqlite:///./db.db"

engine = create_async_engine(
    DATABASE_URL, echo=False, pool_pre_ping=True, connect_args={"timeout": 30}
)


@event.listens_for(engine.sync_engine, "connect")
def set_sqlite_pragma(dbapi_connection, _connection_record):
    """Configures SQLite performance and safety settings on connection."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")  # Concurrent read/write
    cursor.execute("PRAGMA synchronous=NORMAL")  # Reduced disk syncs
    cursor.execute("PRAGMA cache_size=-20000")  # 20MB page cache
    cursor.execute("PRAGMA busy_timeout=10000")  # Lock wait timeout
    cursor.execute("PRAGMA foreign_keys=ON")  # Enforce constraints
    cursor.close()


AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
