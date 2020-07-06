import unittest

from gpiozero.pins.mock import MockFactory
from parameterized import parameterized

from constants import Constants
from motor import Motor
from vehicledevice import VehicleDevice


class MotorTest(unittest.TestCase):

    SOME_PIN_ID = 12
    NEUTRAL = 0.0

    def setUp(self) -> None:
        self.mock_servo = MockFactory(pin_class="mockpwmpin").pin(MotorTest.SOME_PIN_ID)
        self.test_obj = Motor(self.mock_servo)

    def test_should_construct(self):

        self.assertIsInstance(self.test_obj, VehicleDevice)
        self.assertIs(self.mock_servo, self.test_obj.servo_ref)
        self.assertEqual(MotorTest.NEUTRAL, self.test_obj.servo_ref.value)

    @parameterized.expand([
        ("N000", 0.0)
        ,("F100", Constants.MOTOR_FWD_THROTTLE_LIMIT)
        ,("R100", Constants.MOTOR_REV_THROTTLE_LIMIT)
        ,("F050", Constants.MOTOR_FWD_THROTTLE_LIMIT/2)
        ,("R025", Constants.MOTOR_REV_THROTTLE_LIMIT/4)
    ])
    def test_should_set_throttle(self, cmd, expected_value):
        some_random_preexisting_value = 45
        self.test_obj.servo_ref.value = some_random_preexisting_value

        self.test_obj.set_throttle(cmd)

        self.assertEqual(expected_value, self.test_obj.servo_ref.value)

    @parameterized.expand([
        "Z000",
        "F99"
    ])
    def test_should_ignore_malformed_commands(self, cmd):
        some_random_preexisting_value = 45
        self.test_obj.servo_ref.value = some_random_preexisting_value

        self.test_obj.set_throttle(cmd)

        self.assertEqual(45, self.test_obj.servo_ref.value)