from PyQt5.QtWidgets import QGridLayout, QWidget, QPushButton, QLabel, QDoubleSpinBox
from common.command import Command
import logging


class TrimDialog(QWidget):
    """
    Custom widget to edit trim values on the client
    """

    def __init__(self, config_handler, command_handler):
        QWidget.__init__(self)
        self.setWindowTitle("Set Trim")
        self.config_handler = config_handler
        self.command_handler = command_handler

        # Try to create the initial trim command from the config file
        self.command = Command()
        command_json = self.config_handler.get_config_value_or('trim_command', self.command.to_json())
        try:
            self.command.from_json(command_json)
        except Exception as e:
            logging.error("Unable to load trim command from config file")

            # Override the bad config value
            self.config_handler.set_config_value('trim_command', self.command.to_json())

        grid_layout = QGridLayout(self)
        self.lbl_heading_trim = QLabel("Heading Trim:", self)
        self.sb_heading_trim = QDoubleSpinBox(self)
        self.sb_heading_trim.setMaximum(1.0)
        self.sb_heading_trim.setMinimum(-1.0)
        self.sb_heading_trim.setSingleStep(.01)
        self.sb_heading_trim.setValue(self.command.get_heading_trim())

        self.lbl_heading_max = QLabel("Heading Max:", self)
        self.sb_heading_max = QDoubleSpinBox(self)
        self.sb_heading_max.setMaximum(1.0)
        self.sb_heading_max.setMinimum(0.0)
        self.sb_heading_max.setSingleStep(.01)
        self.sb_heading_max.setValue(self.command.get_heading_max())

        self.lbl_heading_min = QLabel("Heading Min:", self)
        self.sb_heading_min = QDoubleSpinBox(self)
        self.sb_heading_min.setMaximum(0.0)
        self.sb_heading_min.setMinimum(-1.0)
        self.sb_heading_min.setSingleStep(.01)
        self.sb_heading_min.setValue(self.command.get_heading_min())

        self.lbl_throttle_fwd_max = QLabel("Max Fwd Throttle:", self)
        self.sb_throttle_fwd_max = QDoubleSpinBox(self)
        self.sb_throttle_fwd_max.setMaximum(1.0)
        self.sb_throttle_fwd_max.setMinimum(0.0)
        self.sb_throttle_fwd_max.setSingleStep(.01)
        self.sb_throttle_fwd_max.setValue(self.command.get_throttle_fwd_max())

        self.lbl_throttle_fwd_min = QLabel("Min Fwd Throttle:", self)
        self.sb_throttle_fwd_min = QDoubleSpinBox(self)
        self.sb_throttle_fwd_min.setMaximum(1.0)
        self.sb_throttle_fwd_min.setMinimum(0.0)
        self.sb_throttle_fwd_min.setSingleStep(.01)
        self.sb_throttle_fwd_min.setValue(self.command.get_throttle_fwd_min())

        self.lbl_throttle_rev_max = QLabel("Max Rev Throttle:", self)
        self.sb_throttle_rev_max = QDoubleSpinBox(self)
        self.sb_throttle_rev_max.setMaximum(0.0)
        self.sb_throttle_rev_max.setMinimum(-1.0)
        self.sb_throttle_rev_max.setSingleStep(.01)
        self.sb_throttle_rev_max.setValue(self.command.get_throttle_rev_max())

        self.lbl_throttle_rev_min = QLabel("Min Rev Throttle:", self)
        self.sb_throttle_rev_min = QDoubleSpinBox(self)
        self.sb_throttle_rev_min.setMaximum(0.0)
        self.sb_throttle_rev_min.setMinimum(-1.0)
        self.sb_throttle_rev_min.setSingleStep(.01)
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

        # Populate the current command
        self.command.set_heading_min(self.sb_heading_min.value())
        self.command.set_heading_max(self.sb_heading_max.value())
        self.command.set_heading_trim(self.sb_heading_trim.value())
        self.command.set_throttle_rev_min(self.sb_throttle_rev_min.value())
        self.command.set_throttle_rev_max(self.sb_throttle_rev_max.value())
        self.command.set_throttle_fwd_min(self.sb_throttle_fwd_min.value())
        self.command.set_throttle_fwd_max(self.sb_throttle_fwd_max.value())

        # Send the command and update the config
        self.command_handler.send_command(self.command)
        self.config_handler.set_config_value('trim_command', self.command.to_json())
