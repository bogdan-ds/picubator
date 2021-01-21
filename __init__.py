from time import sleep
from sensor.dht import DHTSensor
from relays.device import RelayDevice

import config


if __name__ == '__main__':
    last_activated = None
    while True:
        sleep(5)
        dht_sensor = DHTSensor()
        humidity, temperature = dht_sensor.read_data()

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
