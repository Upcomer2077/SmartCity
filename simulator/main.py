"""
SmartCity Sensor Simulator

Генерирует данные от IoT-датчиков и отправляет их в Kafka.
Каждый сенсор генерирует данные каждую секунду.
"""

import json
import os
import time
from typing import Dict, List, Tuple

from dotenv import load_dotenv
from kafka import KafkaProducer
from kafka.errors import KafkaError

# Импорт сенсоров (поддержка запуска как модуля и как скрипта)
try:
    # Если запускаем как модуль из корня проекта: python -m simulator.main
    from simulator.sensors import (
        generate_air_quality,
        generate_temperature,
        generate_traffic,
    )
except ImportError:
    # Если запускаем из директории simulator: python main.py
    from sensors import (
        generate_air_quality,
        generate_temperature,
        generate_traffic,
    )

# Загрузка переменных окружения
load_dotenv()

# Конфигурация из переменных окружения
KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "sensors")
GENERATION_INTERVAL = float(os.getenv("GENERATION_INTERVAL", "1.0"))  # секунды

# Конфигурация сенсоров: список кортежей (sensor_id, type, lat, lon, generator_function)
SENSORS: List[Tuple[str, str, float, float, callable]] = [
    # Traffic sensors
    ("traffic-001", "traffic", 55.7558, 37.6173, generate_traffic),  # Москва, центр
    ("traffic-002", "traffic", 55.7520, 37.6156, generate_traffic),  # Москва, рядом
    ("traffic-003", "traffic", 55.7494, 37.6206,
     generate_traffic),  # Москва, другой район

    # Temperature sensors
    ("temp-001", "temperature", 55.7558, 37.6173, generate_temperature),
    ("temp-002", "temperature", 55.7520, 37.6156, generate_temperature),
    ("temp-003", "temperature", 55.7494, 37.6206, generate_temperature),

    # Air quality sensors
    ("air-001", "air_quality", 55.7558, 37.6173, generate_air_quality),
    ("air-002", "air_quality", 55.7520, 37.6156, generate_air_quality),
    ("air-003", "air_quality", 55.7494, 37.6206, generate_air_quality),
]


def create_kafka_producer() -> KafkaProducer:
    """Создает и возвращает Kafka producer."""
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS.split(","),
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            key_serializer=lambda k: k.encode("utf-8") if k else None,
            # Настройки для надежности
            acks="all",  # Ждем подтверждения от всех реплик
            retries=3,
            max_in_flight_requests_per_connection=1,
        )
        print(f"✓ Kafka producer создан. Сервер: {KAFKA_BOOTSTRAP_SERVERS}")
        return producer
    except Exception as e:
        print(f"✗ Ошибка при создании Kafka producer: {e}")
        raise


def send_sensor_data(producer: KafkaProducer, sensor_data: Dict, topic: str) -> bool:
    """
    Отправляет данные сенсора в Kafka.

    Args:
        producer: Kafka producer
        sensor_data: Данные сенсора
        topic: Имя топика Kafka

    Returns:
        True если успешно, False в случае ошибки
    """
    try:
        # Используем sensor_id в качестве ключа для партиционирования
        sensor_id = sensor_data.get("sensor_id", "unknown")

        future = producer.send(
            topic,
            key=sensor_id,
            value=sensor_data,
        )

        # Опционально: ждем подтверждения (можно убрать для async режима)
        record_metadata = future.get(timeout=10)

        print(
            f"✓ Отправлено: {sensor_data['type']} | "
            f"sensor_id={sensor_id} | "
            f"value={sensor_data['value']} | "
            f"coords={sensor_data['coordinates']} | "
            f"timestamp={sensor_data['timestamp']} | "
            f"partition={record_metadata.partition} | "
            f"offset={record_metadata.offset}"
        )
        return True
    except KafkaError as e:
        print(
            f"✗ Kafka ошибка при отправке данных от {sensor_data.get('sensor_id')}: {e}")
        return False
    except Exception as e:
        print(
            f"✗ Ошибка при отправке данных от {sensor_data.get('sensor_id')}: {e}")
        return False


def generate_all_sensor_data() -> List[Dict]:
    """
    Генерирует данные от всех сенсоров.

    Returns:
        Список словарей с данными сенсоров
    """
    sensor_data_list = []

    for sensor_id, sensor_type, lat, lon, generator_func in SENSORS:
        try:
            data = generator_func(sensor_id, lat, lon)
            sensor_data_list.append(data)
        except Exception as e:
            print(f"✗ Ошибка при генерации данных для {sensor_id}: {e}")

    return sensor_data_list


def run_simulator():
    """Основной цикл симулятора."""
    print("=" * 60)
    print("🚀 SmartCity Sensor Simulator")
    print("=" * 60)
    print(f"Kafka сервер: {KAFKA_BOOTSTRAP_SERVERS}")
    print(f"Топик: {KAFKA_TOPIC}")
    print(f"Интервал генерации: {GENERATION_INTERVAL} сек")
    print(f"Количество сенсоров: {len(SENSORS)}")
    print("=" * 60)

    # Создаем Kafka producer
    producer = None
    try:
        producer = create_kafka_producer()
    except Exception as e:
        print(f"✗ Не удалось создать Kafka producer: {e}")
        print("Убедитесь, что Kafka сервер запущен и доступен.")
        return

    # Основной цикл генерации и отправки данных
    iteration = 0
    try:
        while True:
            iteration += 1
            print(f"\n--- Итерация {iteration} ---")

            # Генерируем данные от всех сенсоров
            sensor_data_list = generate_all_sensor_data()

            # Отправляем данные в Kafka
            success_count = 0
            for sensor_data in sensor_data_list:
                if send_sensor_data(producer, sensor_data, KAFKA_TOPIC):
                    success_count += 1

            print(
                f"Отправлено успешно: {success_count}/{len(sensor_data_list)}")

            # Ждем перед следующей итерацией
            time.sleep(GENERATION_INTERVAL)

    except KeyboardInterrupt:
        print("\n\n⚠ Прерывание пользователем (Ctrl+C)")
    except Exception as e:
        print(f"\n✗ Критическая ошибка: {e}")
    finally:
        # Закрываем producer
        if producer:
            print("\n🔄 Закрытие Kafka producer...")
            producer.flush()  # Отправляем все оставшиеся сообщения
            producer.close()
            print("✓ Kafka producer закрыт")
        print("👋 Симулятор остановлен")


if __name__ == "__main__":
    run_simulator()
