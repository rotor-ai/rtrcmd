from PyQt5.QtGui import QPainter, QImage, QPaintEvent, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QWidget
from client.image_stream_server import ImageStreamServer


class ImageViewer(QWidget):

    def __init__(self, *args, **kwargs):
        super(QWidget, self).__init__(*args, **kwargs)

        self.width = 196
        self.height = 144
        self.setMinimumSize(self.width, self.height)

        # Stored image object
        self.q_image = None

        # Start the image server to receive images from the vehicle
        self.video_stream_server = ImageStreamServer(4000)
        self.video_stream_server.start()
        self.video_stream_server.image_received.connect(self.image_received_slot)

    @pyqtSlot()
    def image_received_slot(self):

        # Pull down the last image from the server and convert to a QImage
        last_image = self.video_stream_server.get_last_image()
        data = last_image.tobytes("raw", "RGB")
        self.q_image = QImage(data, last_image.size[0], last_image.size[1], QImage.Format_RGB888)

        # Force a repaint event
        self.update()

    # This function overrides the paint event, which we can use to paint an image to the screen
    def paintEvent(self, event: QPaintEvent):

        painter = QPainter(self)
        if self.q_image is not None:
            painter.drawImage(event.rect(), self.q_image)
        else:
            painter.drawText(event.rect(), Qt.AlignCenter, "No Image Data")

    def stop_server(self):
        self.video_stream_server.stop()
