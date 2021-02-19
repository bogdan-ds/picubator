from time import sleep
import datetime
import smbus2

from sensor.dht import DHT
from sensor.bme280 import BME280
from relays.device import RelayDevice
from sensor.google_sheets_writer import GoogleSheetsWriter

import config


if __name__ == '__main__':
    last_activated = None
    now = datetime.datetime.now()
    sheets_writer = GoogleSheetsWriter(config.SHEETS_CREDENTIAL_PATH,
                                       config.SPREADSHEET_ID)
    smbus = smbus2.SMBus(config.BME280_PORT)
    while True:
        sleep(5)
        dht_sensor = DHT()
        humidity, temperature = dht_sensor.read_data()
        sheet_value_dict = {
            'Temperature': temperature,
            'Humidity': humidity
        }
        now = dht_sensor.periodic_gsheets_write(
            sheets_writer,
            now=now,
            interval_in_min=30,
            sheet_value_dict=sheet_value_dict)
        bme280_sensor = BME280(config.BME280_ADDRESS, smbus)
        data = bme280_sensor.read_data()
        sheet_value_dict = {
            'Temperature': data.temperature,
            'Humidity': data.humidity
        }
        now = bme280_sensor.periodic_gsheets_write(
            sheets_writer,
            now=now,
            interval_in_min=30,
            sheet_value_dict=sheet_value_dict)

