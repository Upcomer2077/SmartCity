from sensorapi.sensors.baseSensor import BaseSensor
from sqlalchemy import UUID


class SensorRegistry:
    """
    In-memory registry to manage active sensor instances.

    Provides an interface for adding, removing, and toggling sensors
    during the simulation lifecycle.
    """

    def __init__(self, initial_sensor_list: list[BaseSensor]) -> None:
        self._sensors = {s.sensor_sn: s for s in initial_sensor_list}

    def __iter__(self):
        """
        Iterate over currently active sensors only.
        Uses a copy of the registry to prevent errors during runtime modification.
        """
        for s in self._sensors.copy().values():
            if s.is_active:
                yield s

    # TODO: Implement synchronization with the database
    def add(self, sensor: BaseSensor):
        """
        Register a new sensor instance if it doesn't already exist.

        :param ```sensor```: Concrete sensor object to be added.
        """
        if not self._sensors.get(sensor.sensor_sn):
            self._sensors[sensor.sensor_sn] = sensor

    def remove(self, sensor_sn: UUID):
        """
        Remove a sensor from the registry by its serial number.

        :param sensor_sn: UUID of the sensor to be removed.
        """
        self._sensors.pop(sensor_sn)

    def toggle_active(self, sensor_sn: UUID, is_active: bool):
        """
        Enable or disable a sensor's data generation without removing it.

        :param sensor_sn: UUID of the target sensor.
        :param is_active: Desired operational state.
        """
        if self._sensors.get(sensor_sn):
            self._sensors[sensor_sn].is_active = is_active
