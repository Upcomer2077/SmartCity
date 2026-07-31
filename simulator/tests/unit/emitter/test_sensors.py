import asyncio
import re
from abc import ABC
from datetime import datetime
from uuid import uuid4

import pytest
from common.types import SensorBufferType
from emitter.sensors import BaseSensor
from emitter.sensors.air_quality.air_sensor import AirSensor
from emitter.sensors.temperature.temperature_sensor import TemperatureSensor
from emitter.sensors.traffic.traffic_sensor import TrafficSensor


class TestSensors:
    @pytest.fixture(
        params=[TrafficSensor, AirSensor, TemperatureSensor],
    )
    def s_class(self, request) -> BaseSensor:
        return request.param

    @pytest.fixture
    def queue(self):
        return asyncio.Queue[SensorBufferType]()

    @pytest.fixture
    def UUID4_REGEX(self):
        return re.compile(
            r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
            re.I,
        )

    def test_is_base_abstract(self):
        assert issubclass(BaseSensor, ABC)

    def test_is_base_sensor_inheritance(self, s_class):
        assert issubclass(s_class, BaseSensor)

    @pytest.mark.parametrize(
        "sensor_class",
        [TrafficSensor, AirSensor, TemperatureSensor, BaseSensor],
    )
    def test_class_has_slots(self, sensor_class):
        assert hasattr(sensor_class, "__slots__")

    def test_sensor_initialization(self, s_class, queue):
        uuid_val = uuid4()
        is_active = False
        instance: BaseSensor = s_class(uuid_val, queue, is_active)

        assert instance.sensor_sn == uuid_val
        assert instance._buffer == queue
        assert instance.is_active == is_active

    @pytest.mark.parametrize(
        "sn",
        [
            "2db64bc9-0836-47b1-9b63-fb7a3ad30f0a",
            "not-uuid",
            "00000000-0000-1000-8000-000000000000",
        ],
    )
    def test_is_uuid_sn(self, queue, sn, s_class, UUID4_REGEX):
        instance: BaseSensor = s_class(sn, queue)
        assert bool(UUID4_REGEX.match(str(instance.sensor_sn)))

    @pytest.mark.parametrize(
        "is_active",
        [True, False],
    )
    def test_bool_is_active(self, queue, is_active, s_class):
        instance: BaseSensor = s_class(uuid4(), queue, is_active)

        assert isinstance(instance.is_active, bool)

    @pytest.mark.parametrize(
        "is_active",
        [1, "sdf", 0, uuid4(), "", {}, tuple(), []],
    )
    def test_not_bool_is_active(self, queue, is_active, s_class):
        with pytest.raises((ValueError, TypeError)):
            instance: BaseSensor = s_class(uuid4(), queue, is_active)

        assert isinstance(instance.is_active, bool)

    @pytest.mark.parametrize("qu", [asyncio.Queue()])
    def test_queue_instance(self, s_class, qu):
        instance: BaseSensor = s_class(uuid4(), qu, False)
        assert isinstance(instance._buffer, asyncio.Queue)

    @pytest.mark.parametrize("qu", [[], "", 0, tuple(), {}])
    def test_not_queue_instance(self, s_class, qu):
        with pytest.raises((TypeError, ValueError)):
            instance: BaseSensor = s_class(uuid4(), qu, False)

            assert isinstance(instance._buffer, asyncio.Queue)

    def test_push_to_buffer(self, queue, s_class):
        instance: BaseSensor = s_class(uuid4(), queue, False)
        instance.push_to_buffer(
            SensorBufferType(
                {
                    "sensor_sn": instance.sensor_sn,
                    "ts": datetime.now().timestamp(),
                    "value": 1,
                }
            )
        )

        assert queue.qsize() == 1

    def test_generate_sensor_data(self, queue, monkeypatch, s_class):
        instance: BaseSensor = s_class(uuid4(), queue, False)
        monkeypatch.setattr("emitter.sensors.random", lambda: 0.1)
        res = instance._generate_sensor_data()
        assert res is None
        monkeypatch.setattr("emitter.sensors.random", lambda: 0.5)
        res = instance._generate_sensor_data()
        assert res is not None
