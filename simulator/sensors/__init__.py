"""Sensor modules for generating IoT sensor data."""

from .air_quality import generate as generate_air_quality
from .temperature import generate as generate_temperature
from .traffic import generate as generate_traffic

__all__ = [
    "generate_air_quality",
    "generate_temperature",
    "generate_traffic",
]
