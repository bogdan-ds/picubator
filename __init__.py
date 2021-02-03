from time import sleep
import datetime

from sensor.dht import DHTSensor
from relays.device import RelayDevice
from sensor.google_sheets_writer import GoogleSheetsWriter

import config


if __name__ == '__main__':
    last_activated = None
    now = datetime.datetime.now()
    sheets_writer = GoogleSheetsWriter(config.SHEETS_CREDENTIAL_PATH,
                                       config.SPREADSHEET_ID)
    while True:
        sleep(5)
        dht_sensor = DHTSensor()
        humidity, temperature = dht_sensor.read_data()
        if now + datetime.timedelta(minutes=30) > datetime.datetime.now():
            now = datetime.datetime.now()
            sheets_writer.write('Temperature', [now, temperature])
            sheets_writer.write('Humidity', [now, humidifier])

        humidifier = RelayDevice(config.HUMIDIFIER['pin'],
                                 config.HUMIDIFIER['lower_threshold'],
                                 config.HUMIDIFIER['upper_threshold'])
        humidifier.operate_within_thresholds(humidity)

        heating = RelayDevice(config.HEATING['pin'],
                              config.HEATING['lower_threshold'],
                              config.HEATING['upper_threshold'])
        heating.operate_within_thresholds(temperature)

        fan = RelayDevice(config.FAN['pin'])
        last_activated = fan.operate_periodically(
            config.FAN['periodic_interval_hours'],
            config.FAN['duration_min'],
            last_activated)
