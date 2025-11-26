import random
from datetime import datetime
from typing import Dict


def generate(sensor_id: str, lat: float, lon: float) -> Dict:
    """
    Generate traffic density as vehicles per minute (vpm).
    """
    base = random.uniform(10.0, 80.0)
    rush = random.uniform(0.0, 120.0) if random.random(
    ) < 0.3 else random.uniform(0.0, 30.0)
    incidents = random.uniform(-10.0, 10.0)
    value = max(0.0, base + rush + incidents)
    return {
        "sensor_id": sensor_id,
        "type": "traffic",
        "value": round(value, 1),
        "coordinates": {"lat": lat, "lon": lon},
        "timestamp": datetime.now().isoformat() + "Z",
    }
