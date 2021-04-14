import unittest

from ..src.client.game_controller import GameControllerCalibration

class GameControllerCalibrationTest(unittest.TestCase):

    def test_should_init(self):

        subject = GameControllerCalibration()

        self.assertEqual(subject.joystick_boundary, 0)
        self.assertEqual(subject.left_trigger_max, 0)
        self.assertEqual(subject.right_trigger_max, 0)

    def test_should_convert_to_json(self):

        subject = GameControllerCalibration()
        subject.left_trigger_max = 1
        subject.right_trigger_max = 2
        subject.joystick_boundary = 3
        expectedJson = dict()
        expectedJson['left_trigger_max'] = 1
        expectedJson['right_trigger_max'] = 2
        expectedJson['joystick_boundary'] = 3

        json = subject.to_json()

        self.assertDictEqual(json, expectedJson)

