from PyQt5.QtGui import QPainter, QImage, QPaintEvent, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QWidget
from client.image_stream_server import ImageStreamServer


class ImageViewer(QWidget):

    def __init__(self, vehicle_ctl, *args, **kwargs):
        super(QWidget, self).__init__(*args, **kwargs)

        self.width = 196
        self.height = 144
        self.setMinimumSize(self.width, self.height)

        # Stored image object
        self.q_image = None

        self._vehicle_ctl = vehicle_ctl
        self._vehicle_ctl.image_received.connect(self.image_received_slot)

    @pyqtSlot()
    def image_received_slot(self):

        # Pull down the last image from the server and convert to a QImage
        last_image = self._vehicle_ctl.get_last_image()
        if last_image is not None:
            data = last_image.tobytes("raw", "RGB")
            self.q_image = QImage(data, last_image.size[0], last_image.size[1], QImage.Format_RGB888)
        else:
            self.q_image = None

        # Force a repaint event
        self.update()

    # This function overrides the paint event, which we can use to paint an image to the screen
    def paintEvent(self, event: QPaintEvent):

        painter = QPainter(self)
        if self.q_image is not None:
            painter.drawImage(event.rect(), self.q_image)
        else:
            painter.drawText(event.rect(), Qt.AlignCenter, "No Image Data")
