from sqlalchemy import (
    UUID,
    Boolean,
    Float,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class _EdgeBase(DeclarativeBase):
    pass


class EdgeSensorData(_EdgeBase):
    __tablename__ = "edge_buffer"
    ts: Mapped[float] = mapped_column(Float, nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    sensor_id: Mapped[UUID] = mapped_column(UUID, nullable=False, primary_key=True)
    is_pushed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "ts",
            "value",
            "sensor_id",
            name="ts_value_sensor_id",
            sqlite_on_conflict="IGNORE",
        ),
    )


EdgeBase = _EdgeBase
