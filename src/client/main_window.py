from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget, QPushButton, QLineEdit, QLabel, QSpinBox
from PyQt5.QtCore import QSize
from common.command import Command
from client.command_handler import CommandHandler
from common.config_handler import ConfigHandler
from client.trim_dialog import TrimDialog


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        self.config_handler = ConfigHandler()

        self.command = Command()
        self.command_handler = CommandHandler()
        ip = self.config_handler.get_config_value_or('vehicle_ip', "127.0.0.1")
        port = self.config_handler.get_config_value_or('vehicle_port', 5000)
        self.command_handler.set_endpoint(ip, port)

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

        # Give the central widget focus so the key presses work
        central_widget.setFocus()

    def show_trim_window(self):

        self.trim_window = TrimDialog(self.config_handler, self.command_handler)
        self.trim_window.setGeometry(QtCore.QRect(100, 100, 400, 200))
        self.trim_window.show()

    def ip_changed(self, ip):

        port = self.sb_port.value()
        self.command_handler.set_endpoint(ip, port)
        self.config_handler.set_config_value('vehicle_ip', ip)

    def port_changed(self, port):

        ip = self.le_ip.text()
        self.command_handler.set_endpoint(ip, port)
        self.config_handler.set_config_value('vehicle_port', port)

    def keyPressEvent(self, e):
        down = True
        command_changed = False
        if e.key() == QtCore.Qt.Key_Up:

            self.command.throttle = 1.0
            self.up_btn.setDown(down)
            command_changed = True

        if e.key() == QtCore.Qt.Key_Left:

            self.command.heading = -1.0
            self.left_btn.setDown(down)
            command_changed = True

        if e.key() == QtCore.Qt.Key_Down:

            self.command.throttle = -1.0
            self.down_btn.setDown(down)
            command_changed = True

        if e.key() == QtCore.Qt.Key_Right:

            self.command.heading = 1.0
            self.right_btn.setDown(down)
            command_changed = True

        if command_changed:
            self.command_handler.send_command(self.command)

        return super().keyPressEvent(e)

    def keyReleaseEvent(self, e):
        down = False
        command_changed = False
        if e.key() == QtCore.Qt.Key_Up:

            self.command.throttle = 0.0
            self.up_btn.setDown(down)
            command_changed = True

        elif e.key() == QtCore.Qt.Key_Left:

            self.command.heading = 0.0
            self.left_btn.setDown(down)
            command_changed = True

        elif e.key() == QtCore.Qt.Key_Down:

            self.command.throttle = 0.0
            self.down_btn.setDown(down)
            command_changed = True

        elif e.key() == QtCore.Qt.Key_Right:

            self.command.heading = 0.0
            self.right_btn.setDown(down)
            command_changed = True

        if command_changed:
            self.command_handler.send_command(self.command)

        return super().keyReleaseEvent(e)
