import random
from datetime import datetime
from typing import Dict


def generate(sensor_id: str, lat: float, lon: float) -> Dict:
    """
    Generate a temperature sensor reading in Celsius.
    Typical city outdoor range: -20 to 40, with noise.
    """
    base = random.uniform(10.0, 25.0)
    diurnal = random.uniform(-5.0, 5.0)
    noise = random.uniform(-1.0, 1.0)
    value = max(-30.0, min(50.0, base + diurnal + noise))
    return {
        "sensor_id": sensor_id,
        "type": "temperature",
        "value": round(value, 2),
        "coordinates": {"lat": lat, "lon": lon},
        "timestamp": datetime.now().isoformat() + "Z",
    }
