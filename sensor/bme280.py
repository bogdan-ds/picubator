import bme280
import smbus2

from sensor.sensor_base import SensorBase


class BME280(SensorBase):

    def __init__(self, port, address):
        self.port = port
        self.bus = smbus2.SMBus(port)
        self.address = address
        self.calibration_params = bme280.load_calibration_params(self.bus,
                                                                 self.address)

    def read_data(self):
        data = bme280.sample(self.bus, self.address, self.calibration_params)
        return data
