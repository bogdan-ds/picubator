import unittest
import mock
from datetime import datetime, timedelta
import freezegun

MockRPi = mock.MagicMock()
modules = {
    "RPi": MockRPi,
    "RPi.GPIO": MockRPi.GPIO,
}
patcher = mock.patch.dict("sys.modules", modules)
patcher.start()

from relays.device import RelayDevice


class TestRelayDevice(unittest.TestCase):

    def setUp(self):
        self.pin_number = 7
        self.lower_threshold = 36
        self.upper_threshold = 39
        with mock.patch('RPi.GPIO'):
            self.device = RelayDevice(self.pin_number,
                                      self.lower_threshold,
                                      self.upper_threshold)

    def test_set_relay_on_lower_threshold(self):
        MockRPi.GPIO.input.return_value = False
        with mock.patch('relays.device.RelayDevice.set_relay_on') as \
                mocked_relay_on:
            self.device.operate_within_thresholds(35)
        self.assertTrue(mocked_relay_on.called)

    def test_set_relay_on_upper_threshold(self):
        MockRPi.GPIO.input.return_value = True
        with mock.patch('relays.device.RelayDevice.set_relay_off') as \
                mocked_relay_off:
            self.device.operate_within_thresholds(40)
        self.assertTrue(mocked_relay_off.called)

    def test_operate_within_threshold(self):
        MockRPi.GPIO.input.return_value = True
        with mock.patch('relays.device.RelayDevice.set_relay_off') as \
                mocked_relay_off:
            with mock.patch('relays.device.RelayDevice.set_relay_on') as \
                    mocked_relay_on:
                self.device.operate_within_thresholds(37)
                self.assertFalse(mocked_relay_off.called)
                self.assertFalse(mocked_relay_on.called)

    def test_operate_periodically_turn_on(self):
        with mock.patch('relays.device.RelayDevice.set_relay_on') as \
                mocked_relay_on:
            self.device.operate_periodically(2, 3)
            self.assertTrue(mocked_relay_on.called)

    def test_operate_periodically_duration(self):
        with mock.patch('relays.device.RelayDevice.set_relay_off') as \
                mocked_relay_off:
            with mock.patch('relays.device.RelayDevice.is_relay_on') as \
                    mocked_relay_state:
                mocked_relay_state.return_value = True
                last_activated = None
                last_activated = self.device.operate_periodically(
                    2, 3, last_activated)
                with freezegun.freeze_time(datetime.now() +
                                           timedelta(minutes=4)):
                    self.device.operate_periodically(2, 3, last_activated)
                    self.assertTrue(mocked_relay_off.called)

    def test_operate_periodically_interval(self):
        with mock.patch('relays.device.RelayDevice.set_relay_on') as \
                mocked_relay_on:
            with mock.patch('relays.device.RelayDevice.is_relay_on') as \
                    mocked_relay_state:
                mocked_relay_state.return_value = False
                now = datetime.now()
                last_activated = now
                with freezegun.freeze_time(now + timedelta(hours=3)):
                    last_activated = self.device.operate_periodically(
                        2, 3, last_activated)
                    self.assertTrue(mocked_relay_on.called)
