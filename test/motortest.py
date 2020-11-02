import unittest

from gpiozero.pins.mock import MockFactory
from parameterized import parameterized

from vehicle.constants import Constants
from vehicle.throttle import Motor


class MotorTest(unittest.TestCase):

    SOME_PIN_ID = 12
    NEUTRAL = 0.0

    def setUp(self) -> None:
        self.mock_servo = MockFactory(pin_class="mockpwmpin").pin(MotorTest.SOME_PIN_ID)
        self.test_obj = Motor(self.mock_servo)

    def test_should_construct(self):

        self.assertIs(self.mock_servo, self.test_obj.servo_ref)
        self.assertEqual(MotorTest.NEUTRAL, self.test_obj.servo_ref.value)

    @parameterized.expand([
        ("N000", 0.0)
        ,("F100", Constants.MOTOR_FWD_THROTTLE_MAX)
        ,("R100", Constants.MOTOR_REV_THROTTLE_MAX)
        ,("F050", Constants.MOTOR_FWD_THROTTLE_MIN + ((Constants.MOTOR_FWD_THROTTLE_MAX - Constants.MOTOR_FWD_THROTTLE_MIN)/2))
        ,("R025", Constants.MOTOR_REV_THROTTLE_MIN + ((Constants.MOTOR_REV_THROTTLE_MAX - Constants.MOTOR_REV_THROTTLE_MIN)/4))
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