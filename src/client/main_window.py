from PyQt5 import QtCore, Qt
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget, QPushButton, QLineEdit, QLabel, QSpinBox, QComboBox
from PyQt5.QtCore import QSize
from common.command import Command
from client.request_handler import CommandHandler
from common.config_handler import ConfigHandler
from client.trim_dialog import TrimDialog
from common.mode import Mode, ModeType
from client.image_viewer import ImageViewer


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

        self.config_handler = ConfigHandler.get_instance()

        self.request_handler = CommandHandler()
        ip = self.config_handler.get_config_value_or('vehicle_ip', "127.0.0.1")
        port = self.config_handler.get_config_value_or('vehicle_port', 5000)
        self.request_handler.set_endpoint(ip, port)

        # Get the initial command including trim values from the config handler
        self.command = Command()

        # Our popup window for setting trim
        self.trim_window = None

        self.setMinimumSize(QSize(150, 50))
        self.setWindowTitle("Rotor Client")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Need to allow the central widget to get focus so the key presses are caught correctly
        central_widget.setFocusPolicy(QtCore.Qt.ClickFocus)

        # Create all the buttons and widgets
        self.up_btn = QPushButton("FWD", self)
        self.down_btn = QPushButton("REV", self)
        self.left_btn = QPushButton("LEFT", self)
        self.right_btn = QPushButton("RIGHT", self)
        self.trim_btn = QPushButton("Set Trim", self)
        self.trim_btn.clicked.connect(self.show_trim_window)
        self.le_ip = QLineEdit(ip, self)
        self.le_ip.textChanged.connect(self.ip_changed)
        self.lbl_ip = QLabel("Ip:")
        self.sb_port = QSpinBox(self)
        self.sb_port.setMaximum(99999)
        self.sb_port.setValue(port)
        self.sb_port.valueChanged.connect(self.port_changed)
        self.lbl_port = QLabel("Port:")
        self.lbl_mode = QLabel("Mode:")
        self.cbo_mode = QComboBox(self)
        self.cbo_mode.addItem("NORMAL", int(ModeType.NORMAL))
        self.cbo_mode.addItem("TRAIN", int(ModeType.TRAIN))
        self.cbo_mode.addItem("AUTO", int(ModeType.AUTO))
        self.cbo_mode.addItem("ASSISTED", int(ModeType.ASSISTED))

        # Create the image viewer
        self.image_viewer = ImageViewer(self)

        # Connect all the push button signals
        self.up_btn.pressed.connect(self.up_pressed)
        self.up_btn.released.connect(self.up_released)
        self.down_btn.pressed.connect(self.down_pressed)
        self.down_btn.released.connect(self.down_released)
        self.right_btn.pressed.connect(self.right_pressed)
        self.right_btn.released.connect(self.right_released)
        self.left_btn.pressed.connect(self.left_pressed)
        self.left_btn.released.connect(self.left_released)
        self.cbo_mode.activated.connect(self.mode_changed)

        # Set the widgets in the grid layout
        grid_layout = QGridLayout(central_widget)
        grid_layout.addWidget(self.up_btn, 0, 1)
        grid_layout.addWidget(self.left_btn, 1, 0)
        grid_layout.addWidget(self.down_btn, 1, 1)
        grid_layout.addWidget(self.right_btn, 1, 2)
        grid_layout.addWidget(self.trim_btn, 0, 2)
        grid_layout.addWidget(self.lbl_ip, 2, 0)
        grid_layout.addWidget(self.le_ip, 2, 1, 1, 2)  # Stretch the line edit into two cells
        grid_layout.addWidget(self.lbl_port, 3, 0)
        grid_layout.addWidget(self.sb_port, 3, 1, 1, 2)  # Stretch the spinbox into two cells
        grid_layout.addWidget(self.lbl_mode, 4, 0)
        grid_layout.addWidget(self.cbo_mode, 4, 1, 1, 2)
        grid_layout.addWidget(self.image_viewer, 0, 3, 5, 1)

        # Give the central widget focus so the key presses work
        central_widget.setFocus()

    def closeEvent(self, event) -> None:
        self.image_viewer.stop_server()

    def up_pressed(self):
        self.command.set_throttle(1.0)
        self.send_command()

    def up_released(self):
        self.command.set_throttle(0.0)
        self.send_command()

    def down_pressed(self):
        self.command.set_throttle(-1.0)
        self.send_command()

    def down_released(self):
        self.command.set_throttle(0.0)
        self.send_command()

    def right_pressed(self):
        self.command.set_steering(1.0)
        self.send_command()

    def right_released(self):
        self.command.set_steering(0.0)
        self.send_command()

    def left_pressed(self):
        self.command.set_steering(-1.0)
        self.send_command()

    def left_released(self):
        self.command.set_steering(0.0)
        self.send_command()

    def show_trim_window(self):

        # Pull in the trim from the vehicle to populate the trim window
        trim = self.request_handler.get_trim()
        self.trim_window = TrimDialog(trim)
        self.trim_window.setGeometry(QtCore.QRect(100, 100, 400, 200))
        self.trim_window.show()

        # After things have been trimmed, update our command so we can send updated trim values
        self.trim_window.trim_changed.connect(self.update_trim_from_dialog)

    def update_trim_from_dialog(self):
        trim = self.trim_window.get_trim()
        self.request_handler.send_trim(trim)

    def ip_changed(self, ip):

        port = self.sb_port.value()
        self.request_handler.set_endpoint(ip, port)
        self.config_handler.set_config_value('vehicle_ip', ip)

    def port_changed(self, port):

        ip = self.le_ip.text()
        self.request_handler.set_endpoint(ip, port)
        self.config_handler.set_config_value('vehicle_port', port)

    def mode_changed(self, index):
        mode_int = self.cbo_mode.currentData()
        mode = Mode()
        mode.set_mode(mode_int)
        self.request_handler.send_mode(mode)

    def keyPressEvent(self, e):

        if e.key() == QtCore.Qt.Key_Up:
            self.up_pressed()
        if e.key() == QtCore.Qt.Key_Left:
            self.left_pressed()
        if e.key() == QtCore.Qt.Key_Down:
            self.down_pressed()
        if e.key() == QtCore.Qt.Key_Right:
            self.right_pressed()

        return super().keyPressEvent(e)

    def keyReleaseEvent(self, e):

        if e.key() == QtCore.Qt.Key_Up:
            self.up_released()
        elif e.key() == QtCore.Qt.Key_Left:
            self.left_released()
        elif e.key() == QtCore.Qt.Key_Down:
            self.down_released()
        elif e.key() == QtCore.Qt.Key_Right:
            self.right_released()

        return super().keyReleaseEvent(e)

    def send_command(self):
        self.request_handler.send_command(self.command)

    def send_trim(self):
        self.request_handler.send_trim(self.trim)
