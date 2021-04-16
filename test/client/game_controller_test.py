import unittest

from ..context import src
from src.client.game_controller import GameControllerCalibration

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

    def test_from_json_should_populate_all_fields(self):
        inputJson = dict()
        inputJson['left_trigger_max'] = 4
        inputJson['right_trigger_max'] = 5
        inputJson['joystick_boundary'] = 6
        subject = GameControllerCalibration()

        subject.from_json(inputJson)

        self.assertEqual(4, subject.left_trigger_max)
        self.assertEqual(5, subject.right_trigger_max)
        self.assertEqual(6, subject.joystick_boundary)

    def test_from_json_should_handle_all_missing_keys(self):
        subject = GameControllerCalibration()
        subject.left_trigger_max = 1
        subject.right_trigger_max = 2
        subject.joystick_boundary = 3
        inputJson = dict()

        subject.from_json(inputJson)

        self.assertEqual(1, subject.left_trigger_max)
        self.assertEqual(2, subject.right_trigger_max)
        self.assertEqual(3, subject.joystick_boundary)

    def test_from_json_should_handle_individual_missing_keys(self):
        subject = GameControllerCalibration()
        subject.left_trigger_max = 1
        subject.right_trigger_max = 2
        subject.joystick_boundary = 3
        inputJson = dict()
        inputJson['left_trigger_max'] = 11

        subject.from_json(inputJson)

        self.assertEqual(11, subject.left_trigger_max)

        inputJson['right_trigger_max'] = 22
        subject.from_json(inputJson)

        self.assertEqual(22, subject.right_trigger_max)
