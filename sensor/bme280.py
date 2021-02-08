import bme280

from sensor.sensor_base import SensorBase


class BME280(SensorBase):

    def __init__(self, address, smbus):
        self.address = address
        self.bus = smbus
        self.calibration_params = bme280.load_calibration_params(self.bus,
                                                                 self.address)

    def read_data(self):
        data = bme280.sample(self.bus, self.address, self.calibration_params)
        return data
