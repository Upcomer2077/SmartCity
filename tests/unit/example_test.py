import asyncio
from unittest.mock import patch
from uuid import uuid4

import pytest
from broker.brokers.base_broker import BaseBroker
from broker.brokers.kafka_broker import KafkaBroker
from common.types.enums import SensorEnum
from sensorAPI import _get_sensor_type
from sensorAPI.sensors.air_quality.airSensor import AirSensor
from sensorAPI.sensors.temperature.temperatureSensor import TemperatureSensor
from sensorAPI.sensors.traffic.trafficSensor import TrafficSensor

# ========== Тесты для sensorAPI ==========


def test_get_sensor_type_air_quality():
    """Тест функции _get_sensor_type для типа AIR_Q"""
    sensor_class = _get_sensor_type(SensorEnum.AIR_Q)
    assert sensor_class == AirSensor


def test_get_sensor_type_temperature():
    """Тест функции _get_sensor_type для типа TEMP"""
    sensor_class = _get_sensor_type(SensorEnum.TEMP)
    assert sensor_class == TemperatureSensor


def test_get_sensor_type_traffic():
    """Тест функции _get_sensor_type для типа TRAFFIC"""
    sensor_class = _get_sensor_type(SensorEnum.TRAFFIC)
    assert sensor_class == TrafficSensor


def test_base_sensor_initialization():
    """Тест инициализации BaseSensor"""
    sensor_id = uuid4()
    queue = asyncio.Queue()

    # TemperatureSensor наследуется от BaseSensor
    sensor = TemperatureSensor(sensor_id, queue)

    assert sensor.sensor_id == sensor_id
    assert sensor._buffer == queue


def test_temperature_sensor_value_range():
    """Тест генерации данных TemperatureSensor - проверка диапазона значений"""
    sensor_id = uuid4()
    queue = asyncio.Queue()
    sensor = TemperatureSensor(sensor_id, queue)

    # Генерируем несколько значений и проверяем диапазон
    values = []
    for _ in range(100):
        data = sensor._generate_sensor_data()
        if data is not None:
            assert data["sensor_id"] == sensor_id
            assert 20 <= data["value"] <= 30
            assert "ts" in data
            values.append(data["value"])

    # Проверяем, что хотя бы некоторые значения были сгенерированы
    assert len(values) > 0


# ========== Тесты для broker ==========


def test_kafka_broker_initialization_default():
    """Тест инициализации KafkaBroker с дефолтными параметрами"""
    broker = KafkaBroker()
    assert broker._KAFKA_BOOTSTRAP_SERVERS == "localhost:9092"
    assert broker._broker is None  # Еще не инициализирован


def test_kafka_broker_initialization_custom():
    """Тест инициализации KafkaBroker с кастомными серверами"""
    custom_servers = ["server1:9092", "server2:9092"]
    broker = KafkaBroker(custom_servers)
    assert broker._KAFKA_BOOTSTRAP_SERVERS == custom_servers


def test_kafka_broker_get_broker_name():
    """Тест метода get_broker_name для KafkaBroker"""
    broker = KafkaBroker()
    assert broker.get_broker_name() == "Kafka"


def test_base_broker_is_abstract():
    """Тест, что BaseBroker является абстрактным классом"""
    # Попытка создать экземпляр абстрактного класса должна вызвать ошибку
    with pytest.raises(TypeError):
        BaseBroker()


@patch("broker.brokers.kafka_broker.KafkaProducer")
def test_kafka_broker_bring_me_to_life(mock_kafka_producer):
    """Тест метода bring_me_to_life для KafkaBroker"""
    broker = KafkaBroker("test:9092")
    broker.bring_me_to_life()

    # Проверяем, что KafkaProducer был создан с правильными параметрами
    mock_kafka_producer.assert_called_once()
    call_kwargs = mock_kafka_producer.call_args[1]
    assert call_kwargs["bootstrap_servers"] == "test:9092"
    assert call_kwargs["acks"] == 1
    assert call_kwargs["retries"] == 3
    assert call_kwargs["compression_type"] == "gzip"
    assert broker._broker is not None
