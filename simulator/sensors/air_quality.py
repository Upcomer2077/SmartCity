import random
from datetime import datetime
from typing import Dict


def generate(sensor_id: str, lat: float, lon: float) -> Dict:
    """
    Generate air quality reading as AQI-like index (0..500).
    """
    base = random.uniform(20.0, 120.0)
    traffic_impact = random.uniform(0.0, 60.0)
    weather_impact = random.uniform(-10.0, 10.0)
    value = max(0.0, min(500.0, base + traffic_impact + weather_impact))
    return {
        "sensor_id": sensor_id,
        "type": "air_quality",
        "value": round(value, 1),
        "coordinates": {"lat": lat, "lon": lon},
        "timestamp": datetime.now().isoformat() + "Z",
    }
