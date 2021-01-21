import datetime
import logging.config
import RPi.GPIO as GPIO
import config

logging.config.dictConfig(config.log_conf)
LOG = logging.getLogger(__name__)


class RelayDevice:

    def __init__(self, pin_number, lower_threshold=None, upper_threshold=None):
        self.pin_number = pin_number
        self.lower_threshold = lower_threshold
        self.upper_threshold = upper_threshold
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin_number, GPIO.OUT)

    def operate_within_thresholds(self, sensor_reading):
        if sensor_reading < self.lower_threshold and not self.is_relay_on():
            LOG.debug(f'Lower threshold reached '
                      f'at sensor value {sensor_reading}')
            self.set_relay_on()
        elif sensor_reading > self.upper_threshold and self.is_relay_on():
            LOG.debug(f'Upper threshold reached '
                      f'at sensor value {sensor_reading}')
            self.set_relay_off()

    def operate_periodically(self, interval, duration, last_activated=None):
        now = datetime.datetime.now()
        if not last_activated:
            return self.set_relay_on()
        elif last_activated and not self.is_relay_on():
            interval = datetime.timedelta(hours=interval)
            if now - last_activated > interval:
                return self.set_relay_on()
        elif last_activated and self.is_relay_on():
            duration = datetime.timedelta(minutes=duration)
            if now - last_activated > duration:
                return self.set_relay_off()
        return last_activated

    def is_relay_on(self):
        state = GPIO.input(self.pin_number)
        return state

    def set_relay_on(self):
        GPIO.output(self.pin_number, GPIO.HIGH)
        if config.LOG:
            LOG.debug(f'Set relay to ON for device on pin {self.pin_number}')
        last_activated = datetime.datetime.now()
        return last_activated

    def set_relay_off(self):
        GPIO.output(self.pin_number, GPIO.LOW)
        if config.LOG:
            LOG.debug(f'Set relay to OFF for device on pin {self.pin_number}')
        last_activated = datetime.datetime.now()
        return last_activated
