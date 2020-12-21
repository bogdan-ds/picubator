import Adafruit_DHT

import config


class DHTSensor:

    def __init__(self, sensor_type=None, sensor_pin=None):
        self.sensor_type = sensor_type if sensor_type else config.DHT_SENSOR
        self.sensor = getattr(Adafruit_DHT, self.sensor_type, None)
        self.sensor_pin = sensor_pin if sensor_pin else config.DHT_PIN

        if not self.sensor:
            raise Exception(f'Sensor type {self.sensor_type} is invalid')

    def read_data(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor,
                                                        self.sensor_pin)
        if not humidity and not temperature:
            raise Exception('Cannot read from DHT sensor')
        return humidity, temperature

