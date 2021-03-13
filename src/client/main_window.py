from PyQt5 import QtCore, Qt
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget, QPushButton, QLineEdit, QLabel, QSpinBox, QComboBox
from PyQt5.QtCore import QSize
from common.command import Command
from .trim_dialog import TrimDialog
from common.mode import Mode, ModeType
from .image_viewer import ImageViewer


class MainWindow(QMainWindow):

    def __init__(self, vehicle_ctl):
        QMainWindow.__init__(self)

        # Main vehicle control interface
        self._vehicle_ctl = vehicle_ctl

        # Our current command
        self._cmd = Command()

        # Our popup window for setting trim
        self._trim_window = None

        self.setMinimumSize(QSize(150, 50))
        self.setWindowTitle("Rotor Client")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Need to allow the central widget to get focus so the key presses are caught correctly
        central_widget.setFocusPolicy(QtCore.Qt.ClickFocus)

        # Create all the buttons and widgets
        self._up_btn = QPushButton("FWD", self)
        self._down_btn = QPushButton("REV", self)
        self._left_btn = QPushButton("LEFT", self)
        self._right_btn = QPushButton("RIGHT", self)
        self._trim_btn = QPushButton("Set Trim", self)
        self._trim_btn.clicked.connect(self.show_trim_window)
        self._le_ip = QLineEdit(self._vehicle_ctl.vehicle_ip(), self)
        self._le_ip.textChanged.connect(self.ip_changed)
        self._lbl_ip = QLabel("Ip:")
        self._sb_port = QSpinBox(self)
        self._sb_port.setMaximum(99999)
        self._sb_port.setValue(self._vehicle_ctl.vehicle_port())
        self._sb_port.valueChanged.connect(self.port_changed)
        self._lbl_port = QLabel("Port:")
        self._lbl_mode = QLabel("Mode:")
        self._cbo_mode = QComboBox(self)
        self._cbo_mode.addItem("NORMAL", int(ModeType.NORMAL))
        self._cbo_mode.addItem("TRAIN", int(ModeType.TRAIN))
        self._cbo_mode.addItem("AUTO", int(ModeType.AUTO))
        self._btn_restart = QPushButton("Restart Stream")

        # Create the image viewer
        self._image_viewer = ImageViewer(self._vehicle_ctl, self)

        # Connect all the push button signals
        self._up_btn.pressed.connect(self.up_pressed)
        self._up_btn.released.connect(self.up_released)
        self._down_btn.pressed.connect(self.down_pressed)
        self._down_btn.released.connect(self.down_released)
        self._right_btn.pressed.connect(self.right_pressed)
        self._right_btn.released.connect(self.right_released)
        self._left_btn.pressed.connect(self.left_pressed)
        self._left_btn.released.connect(self.left_released)
        self._cbo_mode.activated.connect(self.mode_changed)
        self._btn_restart.pressed.connect(self.restart_stream)

        # Set the widgets in the grid layout
        grid_layout = QGridLayout(central_widget)
        grid_layout.addWidget(self._up_btn, 0, 1)
        grid_layout.addWidget(self._left_btn, 1, 0)
        grid_layout.addWidget(self._down_btn, 1, 1)
        grid_layout.addWidget(self._right_btn, 1, 2)
        grid_layout.addWidget(self._trim_btn, 0, 2)
        grid_layout.addWidget(self._lbl_ip, 2, 0)
        grid_layout.addWidget(self._le_ip, 2, 1, 1, 2)  # Stretch the line edit into two cells
        grid_layout.addWidget(self._lbl_port, 3, 0)
        grid_layout.addWidget(self._sb_port, 3, 1, 1, 2)  # Stretch the spinbox into two cells
        grid_layout.addWidget(self._lbl_mode, 4, 0)
        grid_layout.addWidget(self._cbo_mode, 4, 1, 1, 2)
        grid_layout.addWidget(self._image_viewer, 0, 3, 5, 1)
        grid_layout.addWidget(self._btn_restart, 5, 3)

        # Give the central widget focus so the key presses work
        central_widget.setFocus()

    def up_pressed(self):
        self._cmd.set_throttle(1.0)
        self.send_command()

    def up_released(self):
        self._cmd.set_throttle(0.0)
        self.send_command()

    def down_pressed(self):
        self._cmd.set_throttle(-1.0)
        self.send_command()

    def down_released(self):
        self._cmd.set_throttle(0.0)
        self.send_command()

    def right_pressed(self):
        self._cmd.set_steering(1.0)
        self.send_command()

    def right_released(self):
        self._cmd.set_steering(0.0)
        self.send_command()

    def left_pressed(self):
        self._cmd.set_steering(-1.0)
        self.send_command()

    def left_released(self):
        self._cmd.set_steering(0.0)
        self.send_command()

    def show_trim_window(self):

        # Pull in the trim from the vehicle to populate the trim window
        trim = self._vehicle_ctl.get_trim()
        self._trim_window = TrimDialog(trim)
        self._trim_window.setGeometry(QtCore.QRect(100, 100, 400, 200))
        self._trim_window.show()

        # After things have been trimmed, update our command so we can send updated trim values
        self._trim_window.trim_changed.connect(self.update_trim_from_dialog)

    def update_trim_from_dialog(self):
        trim = self._trim_window.get_trim()
        self._vehicle_ctl.send_trim(trim)

    def ip_changed(self, ip):

        port = self._sb_port.value()
        self._vehicle_ctl.set_endpoint(ip, port)

    def port_changed(self, port):
        ip = self._le_ip.text()
        self._vehicle_ctl.set_endpoint(ip, port)

    def mode_changed(self, index):
        mode_int = self._cbo_mode.currentData()
        mode = Mode()
        mode.set_mode(mode_int)

        self._vehicle_ctl.set_mode(mode)

    def restart_stream(self):

        self._vehicle_ctl.restart_stream()

    def keyPressEvent(self, e):
        if e.isAutoRepeat():
            return super().keyReleaseEvent(e)

        if e.key() == QtCore.Qt.Key_Up or e.key() == QtCore.Qt.Key_W:
            self.up_pressed()
        if e.key() == QtCore.Qt.Key_Left or e.key() == QtCore.Qt.Key_A:
            self.left_pressed()
        if e.key() == QtCore.Qt.Key_Down or e.key() == QtCore.Qt.Key_S:
            self.down_pressed()
        if e.key() == QtCore.Qt.Key_Right or e.key() == QtCore.Qt.Key_D:
            self.right_pressed()

        return super().keyPressEvent(e)

    def keyReleaseEvent(self, e):
        if e.isAutoRepeat():
            return super().keyReleaseEvent(e)

        if e.key() == QtCore.Qt.Key_Up or e.key() == QtCore.Qt.Key_W:
            self.up_released()
        elif e.key() == QtCore.Qt.Key_Left or e.key() == QtCore.Qt.Key_A:
            self.left_released()
        elif e.key() == QtCore.Qt.Key_Down or e.key() == QtCore.Qt.Key_S:
            self.down_released()
        elif e.key() == QtCore.Qt.Key_Right or e.key() == QtCore.Qt.Key_D:
            self.right_released()

        return super().keyReleaseEvent(e)

    def send_command(self):
        self._vehicle_ctl.send_command(self._cmd)

    def send_trim(self):
        self._vehicle_ctl.send_trim(self.trim)
