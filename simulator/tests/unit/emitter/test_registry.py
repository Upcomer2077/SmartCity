from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from emitter.registry import SensorRegistry


class TestSensorRegistry:
    @pytest.fixture
    def mock_sensors(self):
        s1 = MagicMock()
        s1.sensor_sn = uuid4()
        s1.is_active = True

        s2 = MagicMock()
        s2.sensor_sn = uuid4()
        s2.is_active = False

        s3 = MagicMock()
        s3.sensor_sn = uuid4()
        s3.is_active = True

        return [s1, s2, s3]

    def test_registry_initialization_and_len(self, mock_sensors):
        registry = SensorRegistry(mock_sensors)

        assert len(registry) == 3

        for s in mock_sensors:
            assert registry._sensors[s.sensor_sn] is s

    def test_iterator_yields_only_active_sensors(self, mock_sensors):
        registry = SensorRegistry(mock_sensors)

        active_sensors = list(registry)

        assert len(active_sensors) == 2
        assert mock_sensors[0] in active_sensors
        assert mock_sensors[2] in active_sensors
        assert mock_sensors[1] not in active_sensors

    def test_iterator_safe_during_runtime_modification(self, mock_sensors):
        registry = SensorRegistry(mock_sensors)

        try:
            for sensor in registry:
                registry.remove(sensor.sensor_sn)
        except RuntimeError as e:
            pytest.fail(f"{e}")

        assert len(registry) == 1

    def test_iterator_with_no_active_sensors(self, mock_sensors):
        for s in mock_sensors:
            s.is_active = False

        registry = SensorRegistry(mock_sensors)

        assert len(registry) == 3
        assert list(registry) == []
