from PyQt5.QtGui import QPainter, QImage, QPaintEvent
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget


class ImageViewer(QWidget):

    def __init__(self, *args, **kwargs):
        super(QWidget, self).__init__(*args, **kwargs)

        # self.setMinimumSize(20, 100)
        self.width = 196
        self.height = 144
        self.setMinimumSize(self.width, self.height)

        self.image_data = None

    def paintEvent(self, event: QPaintEvent):

        painter = QPainter(self)
        if self.image_data is not None:
            image = QImage()
            image.loadFromData(self.image_data)
            painter.drawImage(event.rect(), image)

        else:
            painter.drawText(event.rect(), Qt.AlignCenter, "No Image Data")

