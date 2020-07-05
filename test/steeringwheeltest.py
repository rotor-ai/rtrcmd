import unittest

from gpiozero.pins.mock import MockFactory

from steeringwheel import SteeringWheel


class SteeringWheelTest(unittest.TestCase):

    SOME_PIN_ID = 13

    def setUp(self) -> None:
        self.mock_servo = MockFactory(pin_class="mockpwmpin").pin(self.SOME_PIN_ID)

    def test_can_construct(self):

        test_obj = SteeringWheel(self.mock_servo)

        self.assertIs(test_obj.servo_ref, self.mock_servo)
