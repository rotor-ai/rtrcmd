import sys
from PyQt5 import QtWidgets
import logging
from client.main_window import MainWindow


if __name__ == "__main__":

    # Set the log level
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create the Qt application and launch
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
