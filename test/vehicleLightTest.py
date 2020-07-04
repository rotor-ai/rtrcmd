import unittest
from unittest.mock import MagicMock, Mock

from constants import Constants
from vehiclelight import VehicleLight


class VehicleLightTest(unittest.TestCase):
    SOME_PIN_ID = 123

    def setUp(self) -> None:
        self.mock_pwmLed = Mock()
        self.mock_pwmLed.value = 0

        self.test_obj = VehicleLight(self.mock_pwmLed)

    def test_should_construct(self):
        self.assertIs(self.mock_pwmLed, self.test_obj.ledRef)
        self.assertFalse(self.test_obj.blinking)
        self.assertEqual(0, self.test_obj.nextBlinkTime)

    def test_should_set_ledRef_value_to_zero(self):
        self.test_obj.ledRef.value = 999

        self.test_obj.set_off()

        self.assertEqual(0, self.test_obj.ledRef.value)

    def test_should_set_ledRef_value_to_dim(self):
        self.test_obj.ledRef.value = 999

        self.test_obj.set_dim()

        self.assertEqual(Constants.LIGHT_DIM_PWM_VAL, self.test_obj.ledRef.value)

    def test_should_set_ledRef_value_to_bright(self):
        self.test_obj.ledRef.value = 999

        self.test_obj.set_bright()

        self.assertEqual(Constants.LIGHT_BRIGHT_PWM_VAL, self.test_obj.ledRef.value)

    def test_should_start_blinking(self):
        self.test_obj.now_wrapper = lambda: 100000000

        self.test_obj.start_blinking()

        self.assertEqual(True, self.test_obj.blinking)
        self.assertEqual(600000000, self.test_obj.nextBlinkTime)
