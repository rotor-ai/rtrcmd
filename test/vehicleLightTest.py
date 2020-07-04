import unittest
from unittest.mock import MagicMock, Mock

from vehiclelight import VehicleLight


class VehicleLightTest(unittest.TestCase):
    SOME_PIN_ID = 123

    def test_should_construct(self):
        mock_pwmLed = Mock()
        mock_pwmLed.value = VehicleLightTest.SOME_PIN_ID

        test_obj = VehicleLight(mock_pwmLed)

        self.assertEqual(VehicleLightTest.SOME_PIN_ID, test_obj.ledRef.value)
        self.assertFalse(test_obj.blinking)
        self.assertEqual(0, test_obj.nextBlinkTime)