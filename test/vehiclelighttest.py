import logging
import unittest

from gpiozero.pins.mock import MockFactory
from vehicle.constants import Constants
from vehicle.vehiclelight import VehicleLight


class VehicleLightTest(unittest.TestCase):
    SOME_PIN_ID = 12

    def assertOnlyLog(self, logs, expectedMsg, expectedLevel = "INFO"):
        self.assertEqual(1, len(logs.records))
        self.assertEqual(expectedLevel, logs.records[0].levelname)
        self.assertEqual(expectedMsg, logs.records[0].message)

    def setUp(self) -> None:
        self.mock_pwmLed = MockFactory(pin_class="mockpwmpin").pin(self.SOME_PIN_ID)
        self.mock_pwmLed.value = 0.5
        self.logger = logging.Logger("some name")
        self.test_obj = VehicleLight(self.logger, self.mock_pwmLed)

    def test_should_construct(self):
        self.assertIs(self.mock_pwmLed, self.test_obj.ledRef)
        self.assertFalse(self.test_obj.blinking)
        self.assertEqual(0, self.test_obj.nextBlinkTime)
        self.assertEqual(0, self.test_obj.ledRef.value)

    def test_set_off(self):
        self.test_obj.blinking = True
        self.test_obj.ledRef.value = 999

        with self.assertLogs(self.logger) as logs:
            self.test_obj.set_off()

        self.assertEqual(0, self.test_obj.ledRef.value)
        self.assertFalse(self.test_obj.blinking)
        self.assertOnlyLog(logs, "Turning off vehicleLight")

    def test_set_dim(self):
        self.test_obj.blinking = True
        self.test_obj.ledRef.value = 999

        with self.assertLogs(self.logger) as logs:
            self.test_obj.set_dim()

        self.assertEqual(Constants.LIGHT_DIM_PWM_VAL, self.test_obj.ledRef.value)
        self.assertFalse(self.test_obj.blinking)
        self.assertOnlyLog(logs, "Setting vehicleLight to dim")

    def test_set_bright(self):
        self.test_obj.blinking = True
        self.test_obj.ledRef.value = 999

        with self.assertLogs(self.logger) as logs:
            self.test_obj.set_bright()

        self.assertEqual(Constants.LIGHT_BRIGHT_PWM_VAL, self.test_obj.ledRef.value)
        self.assertFalse(self.test_obj.blinking)
        self.assertOnlyLog(logs, "Setting vehicleLight to full brightness")

    def test_should_start_blinking(self):
        self.test_obj.now_wrapper = lambda: 100000000

        with self.assertLogs(self.logger) as logs:
            self.test_obj.start_blinking()

        self.assertEqual(True, self.test_obj.blinking)
        self.assertEqual(600000000, self.test_obj.nextBlinkTime)
        self.assertEqual(Constants.LIGHT_BRIGHT_PWM_VAL, self.test_obj.ledRef.value)
        self.assertOnlyLog(logs, "Started blinking vehicleLight")

    def test_should_update_blinker(self):
        self.test_obj.now_wrapper = lambda: 100000000
        self.test_obj.start_blinking()

        self.test_obj.now_wrapper = lambda: 600000000
        self.test_obj.update()

        self.assertEqual(Constants.LIGHT_DIM_PWM_VAL, self.test_obj.ledRef.value)
        self.assertEqual(1100000000, self.test_obj.nextBlinkTime)

        self.test_obj.now_wrapper = lambda: 1100000001
        self.test_obj.update()

        self.assertEqual(Constants.LIGHT_BRIGHT_PWM_VAL, self.test_obj.ledRef.value)
        self.assertEqual(1600000001, self.test_obj.nextBlinkTime)

    def test_should_not_update_blinker_if_duration_has_not_elapsed(self):
        self.test_obj.now_wrapper = lambda: 100000000
        self.test_obj.start_blinking()

        self.test_obj.now_wrapper = lambda: 599999999
        self.test_obj.update()

        self.assertEqual(Constants.LIGHT_BRIGHT_PWM_VAL, self.test_obj.ledRef.value)
        self.assertEqual(600000000, self.test_obj.nextBlinkTime)

    def test_should_not_update_blinker_if_bool_is_false(self):
        self.test_obj.set_bright()
        self.test_obj.blinking = False
        self.test_obj.nextBlinkTime = 123

        self.test_obj.now_wrapper = lambda : 123
        self.test_obj.update()

        self.assertEqual(Constants.LIGHT_BRIGHT_PWM_VAL, self.test_obj.ledRef.value)