from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QGridLayout, QCheckBox, QLabel, QPushButton, QDoubleSpinBox


class TrimDialog(QWidget):
    """
    Custom widget to edit trim values on the client
    """

    trim_changed = Signal()

    def __init__(self, trim):
        QWidget.__init__(self)
        self.setWindowTitle("Set Trim")
        self.trim = trim

        grid_layout = QGridLayout(self)
        self.cb_steering_reversed = QCheckBox("Reverse Steering", self)
        self.cb_steering_reversed.setChecked(self.trim.get_steering_reversed())

        self.lbl_steering_trim = QLabel("Steering Trim:", self)
        self.sb_steering_trim = self.generate_numeric_input(1.0, -1.0, .01, self.trim.get_steering_trim())

        self.lbl_steering_max = QLabel("Steering Max:", self)
        self.sb_steering_max = self.generate_numeric_input(1.0, 0.0, .01, self.trim.get_steering_max())

        self.lbl_steering_min = QLabel("Steering Min:", self)
        self.sb_steering_min = self.generate_numeric_input(0.0, -1.0, .01, self.trim.get_steering_min())

        self.lbl_throttle_trim = QLabel("Throttle Trim:", self)
        self.sb_throttle_trim = self.generate_numeric_input(1.0, -1.0, .01, self.trim.get_throttle_trim())

        self.lbl_throttle_fwd_max = QLabel("Max Fwd Throttle:", self)
        self.sb_throttle_fwd_max = self.generate_numeric_input(1.0, 0.0, .01, self.trim.get_throttle_fwd_max())

        self.lbl_throttle_fwd_min = QLabel("Min Fwd Throttle:", self)
        self.sb_throttle_fwd_min = self.generate_numeric_input(1.0, 0.0, .01, self.trim.get_throttle_fwd_min())

        self.lbl_throttle_rev_max = QLabel("Max Rev Throttle:", self)
        self.sb_throttle_rev_max = self.generate_numeric_input(0.0, -1.0, .01, self.trim.get_throttle_rev_max())

        self.lbl_throttle_rev_min = QLabel("Min Rev Throttle:", self)
        self.sb_throttle_rev_min = self.generate_numeric_input(0.0, -1.0, .01, self.trim.get_throttle_rev_min())

        self.btn_apply = QPushButton("Apply", self)
        self.btn_apply.clicked.connect(self.apply_clicked)

        grid_layout.addWidget(self.cb_steering_reversed, 0, 1)
        grid_layout.addWidget(self.lbl_steering_trim, 1, 0)
        grid_layout.addWidget(self.sb_steering_trim, 1, 1)
        grid_layout.addWidget(self.lbl_steering_max, 2, 0)
        grid_layout.addWidget(self.sb_steering_max, 2, 1)
        grid_layout.addWidget(self.lbl_steering_min, 3, 0)
        grid_layout.addWidget(self.sb_steering_min, 3, 1)
        grid_layout.addWidget(self.lbl_throttle_trim, 4, 0)
        grid_layout.addWidget(self.sb_throttle_trim, 4, 1)
        grid_layout.addWidget(self.lbl_throttle_fwd_max, 5, 0)
        grid_layout.addWidget(self.sb_throttle_fwd_max, 5, 1)
        grid_layout.addWidget(self.lbl_throttle_fwd_min, 6, 0)
        grid_layout.addWidget(self.sb_throttle_fwd_min, 6, 1)
        grid_layout.addWidget(self.lbl_throttle_rev_max, 7, 0)
        grid_layout.addWidget(self.sb_throttle_rev_max, 7, 1)
        grid_layout.addWidget(self.lbl_throttle_rev_min, 8, 0)
        grid_layout.addWidget(self.sb_throttle_rev_min, 8, 1)
        grid_layout.addWidget(self.btn_apply, 9, 1)

    def generate_numeric_input(self, maximum, minimum, increment, current):
        sb = QDoubleSpinBox(self)
        sb.setMaximum(maximum)
        sb.setMinimum(minimum)
        sb.setSingleStep(increment)
        sb.setValue(current)
        return sb

    def apply_clicked(self):

        # Populate the current command
        self.trim.set_steering_min(self.sb_steering_min.value())
        self.trim.set_steering_max(self.sb_steering_max.value())
        self.trim.set_steering_trim(self.sb_steering_trim.value())
        self.trim.set_steering_reversed(self.cb_steering_reversed.isChecked())
        self.trim.set_throttle_trim(self.sb_throttle_trim.value())
        self.trim.set_throttle_rev_min(self.sb_throttle_rev_min.value())
        self.trim.set_throttle_rev_max(self.sb_throttle_rev_max.value())
        self.trim.set_throttle_fwd_min(self.sb_throttle_fwd_min.value())
        self.trim.set_throttle_fwd_max(self.sb_throttle_fwd_max.value())

        self.trim_changed.emit()

    def get_trim(self):
        return self.trim
