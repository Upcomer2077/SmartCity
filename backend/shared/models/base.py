import enum
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ARRAY, TIMESTAMP,  Column, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Admins(Base):
    __tablename__ = "admins"

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String)
    password = Column(String)
    created_at = Column(TIMESTAMP)
    points = relationship("Points", back_populates="admins")


class Points(Base):
    __tablename__ = "points"

    id = Column(Integer, autoincrement=True, primary_key=True)
    sensor_id = Column(Integer, ForeignKey("sensors.sensor_id"))
    title = Column(String)
    created_at = Column(TIMESTAMP)
    created_by = Column(Integer, ForeignKey("admins.id"))
    admins = relationship("Admins", back_populates="points")
    sensors = relationship("Sensors", back_populates="points")


class SensorDataHyper(Base):
    """ """
    __tablename__ = "sensor_data_hyper"
    # id = Column(Integer, autoincrement=True, primary_key=True)
    sensor_id = Column(String, ForeignKey("sensors.sensor_id"))
    data = Column(Float())
    time = Column(TIMESTAMP, primary_key=True)
    sensor = relationship("Sensors", back_populates="sensor_data")


class SensorType(enum.Enum):
    AIR = 0
    TEMPERATURE = 1
    TRAFFIC = 2


class Sensors(Base):
    __tablename__ = "sensors"

    sensor_id = Column(String, primary_key=True)
    created_at = Column(TIMESTAMP)
    type = Column(Enum(SensorType))
    location = Column(ARRAY(Float))
    sensor_data = relationship("SensorDataHyper", back_populates="sensor")
    points = relationship("Points", back_populates="sensors")
