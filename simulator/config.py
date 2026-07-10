from os import getenv

from dotenv import load_dotenv

load_dotenv()

DB_URL = getenv("DB_URL") or ""
KAFKA_BOOTSTRAP_SERVER = getenv("KAFKA_BOOTSTRAP_SERVER") or "localhost:29092"
BROKER_TOPIC = getenv("BROKER_TOPIC") or "telemetry"
