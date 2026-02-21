from datetime import datetime

from sqlalchemy import (
    UUID,
    Boolean,
    Float,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column


class _EdgeBase(DeclarativeBase, MappedAsDataclass):
    pass


class EdgeSensorData(_EdgeBase):
    __tablename__ = "edge_buffer"
    id: Mapped[int] = mapped_column(Integer, name="rowid", primary_key=True, init=False)
    ts: Mapped[datetime] = mapped_column(Float, nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    sensor_sn: Mapped[UUID] = mapped_column(UUID, nullable=False)
    is_pushed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "ts",
            "value",
            "sensor_sn",
            name="ts_value_sensor_sn",
            sqlite_on_conflict="IGNORE",
        ),
    )


EdgeBase = _EdgeBase
