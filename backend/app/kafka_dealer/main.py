import json
from kafka import KafkaConsumer
from typing import TypedDict

from kafka.metrics.stats import Sensor
from sqlalchemy import insert
from sqlalchemy.orm import query
from shared import session, Base, SensorDataHyper, Sensors
consumer = KafkaConsumer('sensors',
                         group_id='my-group',
                         bootstrap_servers=['localhost:9092'])

Coordinates = TypedDict('Coordinates', {'lat': float, 'lon': float})
SensorDataItem = TypedDict('SensorDataItem', {
    'sensor_id': str,
    'type': str,
    'value': float,
    'coordinates': Coordinates,
    'timestamp': str
})


async def kafka_puller():
    print('puller')
    try:
        for message in consumer:
            # message value and key are raw bytes -- decode if necessary!
            # e.g., for unicode: `message.value.decode('utf-8')`
            values: SensorDataItem = json.loads(message.value)
            print(values)

            sensor = session.query(
                Sensors).filter_by(sensor_id=values['sensor_id']).first()
            # print(sensor)
            if sensor:
                # session.add(SensorDataHyper(
                #     sensor_id=values['sensor_id'], data=values['value'], time=values['timestamp']))
                insert(SensorDataHyper).values(sensor_id=values['sensor_id'], data=values['value'], time=values['timestamp']).on_conflict_do_nothing(
                    index_elements=["id"])
                session.commit()

    except Exception as e:
        print(e)
        session.rollback()
