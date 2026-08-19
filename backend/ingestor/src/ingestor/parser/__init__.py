from ingestor.sensor_data_pb2 import BulkIngestionPayload
from ingestor.types import AvailableSensors, SensorDataBatch


class ProtoParser:
    def __init__(self):
        self._telemetry_package: BulkIngestionPayload = BulkIngestionPayload()
        self._data: list[SensorDataBatch] = []

    def _parse_data(self, value: bytes):
        self._data = []
        self._telemetry_package.ParseFromString(value)
        for record in self._telemetry_package.batches:
            sensor_an = record.sensor_sn
            type = record.type
            lat = record.lat
            lon = record.lon
            data = record.data

            self._data.append(
                SensorDataBatch(
                    sn=sensor_an,
                    type=AvailableSensors(type),
                    lat=lat,
                    lon=lon,
                    data=data,
                )
            )
        self._telemetry_package.Clear()

    def get_data_from_bytes(self, value: bytes) -> list[SensorDataBatch]:
        self._parse_data(value)
        return self._data
