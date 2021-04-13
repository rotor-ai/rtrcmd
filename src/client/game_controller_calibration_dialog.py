import logging

import inputs
from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QWidget, QGridLayout, QLabel

from src.client.game_controller import GameController, GameControllerCalibration


class GameControllerCalibrationDialog(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Controller Calibration")

        self._controller_calibration = GameControllerCalibration()
        self.calibration_complete_response = lambda calibration_data: True #replace this lambda with an action you would like to perform when calibration is finished

        grid_layout = QGridLayout(self)

        self.lbl_dialog_text = QLabel(
            "Controller Detected!\nPress the left and right triggers all the way down,\n then press A",
            self)

        self._game_controller = GameController(inputs.devices.gamepads[0])
        self._game_controller.add_event_response('ABS_Z', self.gamepad_left_trigger_response)
        self._game_controller.add_event_response('ABS_RZ', self.gamepad_right_trigger_response)
        self._game_controller.add_event_response('BTN_SOUTH', self.gamepad_a_button_response)

        self.lbl_left_trigger = QLabel("Left Trigger Max Value: ", self)
        self.lbl_left_trigger_value = QLabel(str(self._controller_calibration.left_trigger_max), self)
        self.lbl_right_trigger = QLabel("Right Trigger Max Value: ", self)
        self.lbl_right_trigger_value = QLabel(str(self._controller_calibration.left_trigger_max), self)

        grid_layout.addWidget(self.lbl_dialog_text, 0, 0)
        grid_layout.addWidget(self.lbl_left_trigger, 1,0)
        grid_layout.addWidget(self.lbl_left_trigger_value, 1,1)
        grid_layout.addWidget(self.lbl_right_trigger, 2,0)
        grid_layout.addWidget(self.lbl_right_trigger_value, 2,1)

        self._game_controller.start()

    def gamepad_left_trigger_response(self, state):
        if state > self._controller_calibration.left_trigger_max:
            self._controller_calibration.left_trigger_max = state
            self.lbl_left_trigger_value.setText(str(self._controller_calibration.left_trigger_max))

    def gamepad_right_trigger_response(self, state):
        if state > self._controller_calibration.right_trigger_max:
            self._controller_calibration.right_trigger_max = state
            self.lbl_right_trigger_value.setText(str(self._controller_calibration.right_trigger_max))

    def gamepad_a_button_response(self, state):
        if state == 1:
            self._game_controller.stop()
            self.calibration_complete_response(self._controller_calibration)

