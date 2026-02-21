import uuid
from datetime import datetime

from sqlalchemy import (
    TIMESTAMP,
    UUID,
    VARCHAR,
    Boolean,
    Enum,
    Float,
    ForeignKey,
    Integer,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
    relationship,
)
from sqlalchemy.sql.functions import now

from common.types import SensorType


class _TSBase(DeclarativeBase, MappedAsDataclass):
    pass


class Admins(_TSBase):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, primary_key=True, init=False
    )
    username: Mapped[str] = mapped_column(VARCHAR(32), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(VARCHAR(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, default=now()
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    points: Mapped[list["Points"]] = relationship(back_populates="admin", init=False)
    sensors: Mapped[list["Sensors"]] = relationship(back_populates="admin", init=False)


class Points(_TSBase):
    __tablename__ = "map_points"

    created_by: Mapped[int] = mapped_column(
        Integer, ForeignKey("admins.id", ondelete="SET NULL"), nullable=True
    )
    title: Mapped[str] = mapped_column(VARCHAR(32), nullable=False, unique=True)
    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=now(), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    admin: Mapped["Admins"] = relationship(back_populates="points", init=False)
    bound_sensors: Mapped[list["BoundSensors"]] = relationship(
        back_populates="point", init=False
    )


class Sensors(_TSBase):
    __tablename__ = "sensors"

    type: Mapped[SensorType] = mapped_column(Enum(SensorType), nullable=False)
    lon: Mapped[float] = mapped_column(Float, nullable=False)
    lat: Mapped[float] = mapped_column(Float, nullable=False)
    serial_number: Mapped[UUID] = mapped_column(UUID, unique=True, nullable=False)
    created_by: Mapped[int] = mapped_column(
        Integer, ForeignKey("admins.id", ondelete="SET NULL"), nullable=True
    )
    sensor_id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=now(), nullable=False, onupdate=now()
    )
    sensor_data: Mapped[list["SensorDataHyper"]] = relationship(
        back_populates="sensor", init=False
    )
    bound_points: Mapped[list["BoundSensors"]] = relationship(
        back_populates="sensor", init=False
    )
    admin: Mapped["Admins"] = relationship(back_populates="sensors", init=False)


class SensorDataHyper(_TSBase):
    __tablename__ = "sensor_hyper_data"
    sensor_id: Mapped[UUID] = mapped_column(UUID, ForeignKey("sensors.sensor_id"))
    value: Mapped[float] = mapped_column(Float, nullable=False)
    ts: Mapped[datetime] = mapped_column(TIMESTAMP)
    sensor: Mapped["Sensors"] = relationship(back_populates="sensor_data", init=False)

    __table_args__ = (PrimaryKeyConstraint("ts", "sensor_id", name="PK_ts_sensor_id"),)


class BoundSensors(_TSBase):
    __tablename__ = "bound_sensors"

    map_point_id: Mapped[UUID] = mapped_column(
        UUID, ForeignKey("map_points.id"), nullable=False
    )
    sensor_id: Mapped[UUID] = mapped_column(
        UUID, ForeignKey("sensors.sensor_id"), nullable=False
    )
    point: Mapped["Points"] = relationship(back_populates="bound_sensors", init=False)
    sensor: Mapped["Sensors"] = relationship(back_populates="bound_points", init=False)

    __table_args__ = (
        PrimaryKeyConstraint(
            "map_point_id", "sensor_id", name="PK_map_point_id_sensor_id"
        ),
    )


TSBase = _TSBase
