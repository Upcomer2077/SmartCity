import uuid
from datetime import datetime

from sqlalchemy import Boolean, Enum, ForeignKey, Index, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column
from sqlalchemy.sql.functions import now
from sqlalchemy.types import UUID, Float, Uuid

from common.types.enums import AvailableSensors


class _Base(MappedAsDataclass, DeclarativeBase):
    pass


class Sensor(_Base):
    """
    Registry for physical sensors.
    Stores location, type, and operational status.
    """

    __tablename__ = "sensors"

    lat: Mapped[float] = mapped_column(Float, nullable=False)
    lon: Mapped[float] = mapped_column(Float, nullable=False)
    type: Mapped[AvailableSensors] = mapped_column(
        Enum(AvailableSensors), nullable=False
    )
    serial_number: Mapped[UUID] = mapped_column(
        Uuid, primary_key=True, default=uuid.uuid4
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=now(), init=False)

    __table_args__ = (Index("idx_sensors_lat_lon", "lat", "lon", "type", unique=True),)


class SensorData(_Base):
    """
    Time-series storage for sensor measurements.
    Maps to SQLite rowid for primary key efficiency.
    """

    __tablename__ = "sensor_data"
    id: Mapped[int] = mapped_column(Integer, name="rowid", primary_key=True, init=False)
    ts: Mapped[datetime] = mapped_column(Float, nullable=False, init=False)
    sensor_sn: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("sensors.serial_number", ondelete="CASCADE", name="fkssn"),
        nullable=False,
        init=False,
    )
    value: Mapped[float] = mapped_column(Float, nullable=False, init=False)
    is_delivered: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, init=False
    )

    __table_args__ = (
        Index("idx_sensordata_sensor_ts", "sensor_sn", "ts", unique=True),
    )
