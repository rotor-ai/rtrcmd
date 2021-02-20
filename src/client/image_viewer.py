from PyQt5.QtGui import QPainter, QImage, QPaintEvent, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot, QSize
from PyQt5.QtWidgets import QWidget, QSizePolicy, QBoxLayout, QSpacerItem


class ImageWidget(QWidget):
    """
    Widget responsible for painting the image
    """

    def __init__(self, vehicle_ctl, width, height, *args, **kwargs):
        super(QWidget, self).__init__(*args, **kwargs)

        self._width = width
        self._height = height

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

    def sizeHint(self):

        return QSize(self._width, self._height)


class ImageViewer(QWidget):
    """
    Defines a container for the image view widget with a fixed aspect ratio
    """

    def __init__(self, vehicle_ctl, *args, **kwargs):
        super(QWidget, self).__init__(*args, **kwargs)

        self._width = 196
        self._height = 144
        self._aspect_ratio = self._width / self._height

        size_policy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.setSizePolicy(size_policy)

        layout = QBoxLayout(QBoxLayout.LeftToRight, self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self._image_widget = ImageWidget(vehicle_ctl, self._width, self._height)

        #  add spacer, then widget, then spacer
        self.layout().addItem(QSpacerItem(0, 0))
        self.layout().addWidget(self._image_widget)
        self.layout().addItem(QSpacerItem(0, 0))

    def resizeEvent(self, e):
        w = e.size().width()
        h = e.size().height()

        if w < self._width:
            return
        elif h < self._height:
            return

        if w / h > self._aspect_ratio:  # too wide
            self.layout().setDirection(QBoxLayout.LeftToRight)
            widget_stretch = h * self._aspect_ratio
            outer_stretch = (w - widget_stretch) / 2 + 0.5
        else:  # too tall
            self.layout().setDirection(QBoxLayout.TopToBottom)
            widget_stretch = w / self._aspect_ratio
            outer_stretch = (h - widget_stretch) / 2 + 0.5

        self.layout().setStretch(0, outer_stretch)
        self.layout().setStretch(1, widget_stretch)
        self.layout().setStretch(2, outer_stretch)
