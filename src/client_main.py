import sys
from PyQt5 import QtWidgets
import logging
from client.main_window import MainWindow
from client.vehicle_ctl import VehicleCtl


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
    res = app.exec_()

    # Stop the vehicle control class
    vehicle_ctl.stop()

    # Exit the app
    sys.exit(res)
