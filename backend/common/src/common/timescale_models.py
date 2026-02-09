from datetime import datetime

from sqlalchemy import (
    TIMESTAMP,
    Integer,
    String,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class _TSBase(DeclarativeBase):
    pass


class Admins(_TSBase):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    username: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    # points: Mapped["Points"] = relationship(back_populates="admins")


# class Points(_TSBase):
#     __tablename__ = "points"

#     id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
#     sensor_id: Mapped[int] = mapped_column(Integer, ForeignKey("sensors.sensor_id"))
#     title: Mapped[str] = mapped_column(String)
#     created_at: Mapped[datetime] = mapped_column(TIMESTAMP)
#     created_by: Mapped[int] = mapped_column(Integer, ForeignKey("admins.id"))
#     admins: Mapped["Admins"] = relationship(back_populates="points")
#     sensors: Mapped["Sensors"] = relationship(back_populates="points")


# class SensorDataHyper(_TSBase):
#     """ """

#     __tablename__ = "sensor_data_hyper"
#     # id = Column(Integer, autoincrement=True, primary_key=True)
#     sensor_id: Mapped[str] = mapped_column(String, ForeignKey("sensors.sensor_id"))
#     data: Mapped[float] = mapped_column(Float())
#     time: Mapped[datetime] = mapped_column(TIMESTAMP, primary_key=True)
#     sensor: Mapped["Sensors"] = relationship(back_populates="sensor_data")


# class SensorType(enum.Enum):
#     AIR = 0
#     TEMPERATURE = 1
#     TRAFFIC = 2


# class Sensors(_TSBase):
#     __tablename__ = "sensors"

#     sensor_id: Mapped[str] = mapped_column(String, primary_key=True)
#     created_at: Mapped[datetime] = mapped_column(TIMESTAMP)
#     type: Mapped[SensorType] = mapped_column(Enum(SensorType))
#     lon: Mapped[float] = mapped_column(Float, nullable=False)
#     lat: Mapped[float] = mapped_column(Float, nullable=False)
#     sensor_data: Mapped["SensorDataHyper"] = relationship(back_populates="sensor")
#     points: Mapped["Points"] = relationship(back_populates="sensors")


TSBase = _TSBase
