import logging
import unittest

from gpiozero.pins.mock import MockFactory
from parameterized import parameterized

from constants import Constants
from steeringwheel import SteeringWheel


class SteeringWheelTest(unittest.TestCase):

    SOME_PIN_ID = 13

    def setUp(self) -> None:
        self.mock_servo = MockFactory(pin_class="mockpwmpin").pin(SteeringWheelTest.SOME_PIN_ID)
        self.logger = logging.Logger("some name")
        self.test_obj = SteeringWheel(self.logger, self.mock_servo)

    def test_can_construct(self):

        self.assertIs(self.test_obj.servo_ref, self.mock_servo)
        self.assertEqual(Constants.SERVO_CENTER_PWM_VALUE, self.test_obj.servo_ref.value)

    @parameterized.expand([
        ('N000', Constants.SERVO_CENTER_PWM_VALUE)
        ,('L100', 1)
        ,('R100', -1)
    ])
    def test_can_map_direction_to_servo_value(self, cmd, expected_value):
        with self.assertLogs(self.logger) as logs:
            self.test_obj.set_heading(cmd)

        self.assertEqual(expected_value, self.test_obj.servo_ref.value)
        self.assertEqual("Setting heading to " + cmd, logs.records[0].message)

    def test_can_interpolate_values_based_on_configured_servo_center(self):

        self.test_obj.set_heading('L050')
        expected_value = (1 - Constants.SERVO_CENTER_PWM_VALUE)/2 + Constants.SERVO_CENTER_PWM_VALUE
        self.assertEqual(expected_value, self.test_obj.servo_ref.value)

        self.test_obj.set_heading('R025')
        expected_value = (-1 - Constants.SERVO_CENTER_PWM_VALUE)/4 + Constants.SERVO_CENTER_PWM_VALUE
        self.assertEqual(expected_value, self.test_obj.servo_ref.value)

    def test_should_set_to_center_if_neutral(self):

        self.test_obj.set_heading('N100')
        self.assertEqual(Constants.SERVO_CENTER_PWM_VALUE, self.test_obj.servo_ref.value)

    @parameterized.expand([
        "Z000"
        ,"N99"
    ])
    def test_should_ignore_malformed_command(self, cmd):
        some_random_preexisting_value = 0.45
        self.test_obj.servo_ref.value = some_random_preexisting_value
        l = self.logger

        with self.assertLogs(self.logger) as logs:
            l.info("this-should-be-the-only-log")
            self.test_obj.set_heading(cmd)

        self.assertEqual(0.45, self.test_obj.servo_ref.value)
        self.assertEqual(1, len(logs.records))


