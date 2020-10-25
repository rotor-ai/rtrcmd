import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget, QPushButton
from PyQt5.QtCore import QSize
from command import Command
import requests


class Arrows(QMainWindow):

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

        grid_layout.addWidget(self.up_btn, 0, 1)
        grid_layout.addWidget(self.left_btn, 1, 0)
        grid_layout.addWidget(self.down_btn, 1, 1)
        grid_layout.addWidget(self.right_btn, 1, 2)

        self.command = Command()
        self.ip = "http://127.0.0.1:5000/api"

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

        self.send_updated_command()
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

        self.send_updated_command()
        return super().keyReleaseEvent(e)

    def send_updated_command(self):
        try:
            r = requests.post(self.ip, None, self.command.to_json_string())
            if r.status_code != 200:
                print(r.text)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = Arrows()
    mainWin.show()
    sys.exit(app.exec_())
