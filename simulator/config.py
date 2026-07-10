from os import getenv

from dotenv import load_dotenv

load_dotenv()

DB_URL = getenv("DB_URL") or ""
"""str: Database connection URL string. Defaults to an empty string."""

KAFKA_BOOTSTRAP_SERVER = getenv("KAFKA_BOOTSTRAP_SERVER") or "localhost:29092"
"""str: Kafka bootstrap server address. Defaults to 'localhost:29092'."""

BROKER_TOPIC = getenv("BROKER_TOPIC") or "telemetry"
"""str: Kafka topic name for telemetry data. Defaults to 'telemetry'."""
