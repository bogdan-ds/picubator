import unittest
import mock

from sensor.dht import DHTSensor


class TestDHTSensor(unittest.TestCase):

    def test_initialize(self):
        dht = DHTSensor()
        self.assertTrue(dht.sensor)

    def test_read(self):
        dht = DHTSensor()
        with mock.patch('Adafruit_DHT.read_retry') as mocked_sensor:
            mocked_sensor.return_value = 71.5, 14.800000190734863
            humidity, temperature = dht.read_data()
        self.assertEqual(humidity, 71.5)
