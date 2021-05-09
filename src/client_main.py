import sys
import logging

import inputs
from PySide2 import QtWidgets

from client.main_window import MainWindow
from client.vehicle_ctl import VehicleCtl
from client.game_controller import GameControllerCalibration
from common.config_handler import ConfigHandler

if __name__ == "__main__":

    # Set the log level
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Setup the primary vehicle control class
    vehicle_ctl = VehicleCtl()
    vehicle_ctl.start()

    # Create the Qt application and launch
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow(vehicle_ctl)
    mainWin.show()

    calibration_json = ConfigHandler.get_instance().get_config_value_or('game_controller_calibration', {})
    controllerHasBeenCalibrated = calibration_json != {}
    controllerIsPluggedIn = len(inputs.devices.gamepads) > 0

    if controllerIsPluggedIn and not controllerHasBeenCalibrated:
        mainWin.game_controller_calibration_dialog()
    elif controllerIsPluggedIn and controllerHasBeenCalibrated:
        game_controller_calibration = GameControllerCalibration()
        game_controller_calibration.from_json(calibration_json)
        mainWin.game_controller_calibrated(game_controller_calibration)

    res = app.exec_()

    # Stop the vehicle control class
    vehicle_ctl.stop()

    # Exit the app
    sys.exit(res)
