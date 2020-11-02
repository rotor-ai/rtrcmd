import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget, QPushButton, QLabel, QDoubleSpinBox
from PyQt5.QtCore import QSize
from command import Command
from config_handler import ConfigHandler
from command_handler import CommandHandler
import logging


class TrimDialog(QWidget):

    def __init__(self, command_handler):
        QWidget.__init__(self)
        self.setWindowTitle("Set Trim")
        self.config_handler = ConfigHandler()
        self.command = self.config_handler.get_config_command()
        self.command_handler = command_handler

        grid_layout = QGridLayout(self)
        self.lbl_heading_trim = QLabel("Heading Trim:", self)
        self.sb_heading_trim = QDoubleSpinBox(self)
        self.sb_heading_trim.setMaximum(1.0)
        self.sb_heading_trim.setMinimum(-1.0)
        self.sb_heading_trim.setValue(self.command.get_heading_trim())

        self.lbl_heading_max = QLabel("Heading Max:", self)
        self.sb_heading_max = QDoubleSpinBox(self)
        self.sb_heading_max.setMaximum(1.0)
        self.sb_heading_max.setMinimum(0.0)
        self.sb_heading_max.setValue(self.command.get_heading_max())

        self.lbl_heading_min = QLabel("Heading Min:", self)
        self.sb_heading_min = QDoubleSpinBox(self)
        self.sb_heading_min.setMaximum(0.0)
        self.sb_heading_min.setMinimum(-1.0)
        self.sb_heading_min.setValue(self.command.get_heading_min())

        self.lbl_throttle_fwd_max = QLabel("Max Fwd Throttle:", self)
        self.sb_throttle_fwd_max = QDoubleSpinBox(self)
        self.sb_throttle_fwd_max.setMaximum(1.0)
        self.sb_throttle_fwd_max.setMinimum(0.0)
        self.sb_throttle_fwd_max.setValue(self.command.get_throttle_fwd_max())

        self.lbl_throttle_fwd_min = QLabel("Min Fwd Throttle:", self)
        self.sb_throttle_fwd_min = QDoubleSpinBox(self)
        self.sb_throttle_fwd_min.setMaximum(1.0)
        self.sb_throttle_fwd_min.setMinimum(0.0)
        self.sb_throttle_fwd_min.setValue(self.command.get_throttle_fwd_min())

        self.lbl_throttle_rev_max = QLabel("Max Rev Throttle:", self)
        self.sb_throttle_rev_max = QDoubleSpinBox(self)
        self.sb_throttle_rev_max.setMaximum(0.0)
        self.sb_throttle_rev_max.setMinimum(-1.0)
        self.sb_throttle_rev_max.setValue(self.command.get_throttle_rev_max())

        self.lbl_throttle_rev_min = QLabel("Min Rev Throttle:", self)
        self.sb_throttle_rev_min = QDoubleSpinBox(self)
        self.sb_throttle_rev_min.setMaximum(0.0)
        self.sb_throttle_rev_min.setMinimum(-1.0)
        self.sb_throttle_rev_min.setValue(self.command.get_throttle_rev_min())

        self.btn_apply = QPushButton("Apply", self)
        self.btn_apply.clicked.connect(self.apply_clicked)

        grid_layout.addWidget(self.lbl_heading_trim, 0, 0)
        grid_layout.addWidget(self.sb_heading_trim, 0, 1)
        grid_layout.addWidget(self.lbl_heading_max, 1, 0)
        grid_layout.addWidget(self.sb_heading_max, 1, 1)
        grid_layout.addWidget(self.lbl_heading_min, 2, 0)
        grid_layout.addWidget(self.sb_heading_min, 2, 1)
        grid_layout.addWidget(self.lbl_throttle_fwd_max, 3, 0)
        grid_layout.addWidget(self.sb_throttle_fwd_max, 3, 1)
        grid_layout.addWidget(self.lbl_throttle_fwd_min, 4, 0)
        grid_layout.addWidget(self.sb_throttle_fwd_min, 4, 1)
        grid_layout.addWidget(self.lbl_throttle_rev_max, 5, 0)
        grid_layout.addWidget(self.sb_throttle_rev_max, 5, 1)
        grid_layout.addWidget(self.lbl_throttle_rev_min, 6, 0)
        grid_layout.addWidget(self.sb_throttle_rev_min, 6, 1)
        grid_layout.addWidget(self.btn_apply, 7, 1)

    def apply_clicked(self):

        self.command.set_heading_min(self.sb_heading_min.value())
        self.command.set_heading_max(self.sb_heading_max.value())
        self.command.set_heading_trim(self.sb_heading_trim.value())
        self.command.set_throttle_rev_min(self.sb_throttle_rev_min.value())
        self.command.set_throttle_rev_max(self.sb_throttle_rev_max.value())
        self.command.set_throttle_fwd_min(self.sb_throttle_fwd_min.value())
        self.command.set_throttle_fwd_max(self.sb_throttle_fwd_max.value())

        self.command_handler.send_command(self.command)
        self.config_handler.write_to_config(self.command)


class Buttons(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(150, 50))
        self.setWindowTitle("Rotor Client")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        grid_layout = QGridLayout(central_widget)

        self.up_btn = QPushButton("FWD", self)
        self.down_btn = QPushButton("REV", self)
        self.left_btn = QPushButton("LEFT", self)
        self.right_btn = QPushButton("RIGHT", self)
        self.trim_btn = QPushButton("Set Trim", self)
        self.trim_btn.clicked.connect(self.show_trim_window)

        grid_layout.addWidget(self.up_btn, 0, 1)
        grid_layout.addWidget(self.left_btn, 1, 0)
        grid_layout.addWidget(self.down_btn, 1, 1)
        grid_layout.addWidget(self.right_btn, 1, 2)
        grid_layout.addWidget(self.trim_btn, 0, 2)

        self.command = Command()
        self.command_handler = CommandHandler("http://127.0.0.1:5000/command")

        self.trim_window = None

    def show_trim_window(self):

        self.trim_window = TrimDialog(self.command_handler)
        self.trim_window.setGeometry(QtCore.QRect(100, 100, 400, 200))
        self.trim_window.show()

    def keyPressEvent(self, e):
        down = True
        if e.key() == QtCore.Qt.Key_Up:

            self.command.throttle = 1.0
            self.up_btn.setDown(down)

        if e.key() == QtCore.Qt.Key_Left:

            self.command.heading = -1.0
            self.left_btn.setDown(down)

        if e.key() == QtCore.Qt.Key_Down:

            self.command.throttle = -1.0
            self.down_btn.setDown(down)

        if e.key() == QtCore.Qt.Key_Right:

            self.command.heading = 1.0
            self.right_btn.setDown(down)

        self.command_handler.send_command(self.command)
        return super().keyPressEvent(e)

    def keyReleaseEvent(self, e):
        down = False
        if e.key() == QtCore.Qt.Key_Up:

            self.command.throttle = 0.0
            self.up_btn.setDown(down)

        elif e.key() == QtCore.Qt.Key_Left:

            self.command.heading = 0.0
            self.left_btn.setDown(down)

        elif e.key() == QtCore.Qt.Key_Down:

            self.command.throttle = 0.0
            self.down_btn.setDown(down)

        elif e.key() == QtCore.Qt.Key_Right:

            self.command.heading = 0.0
            self.right_btn.setDown(down)

        self.command_handler.send_command(self.command)
        return super().keyReleaseEvent(e)




if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    app = QtWidgets.QApplication(sys.argv)
    mainWin = Buttons()
    mainWin.show()
    sys.exit(app.exec_())
