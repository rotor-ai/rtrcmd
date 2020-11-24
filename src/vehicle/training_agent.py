from common.config_handler import ConfigHandler
from datetime import datetime
from pathlib import Path
import logging


class TrainingAgent(object):
    """
    The training agent is responsible for saving a metadata file containing sensor information and command information
    in order to train a model
    """

    def __init__(self):
        self.config_handler = ConfigHandler.get_instance()
        self.data_dir = self.config_handler.get_config_value_or('data_dir', '/data')
        self.filepath = None

    def init_new_log(self):
        filename = Path(datetime.now().strftime("%d%m%Y_%H%M%S.json"))
        self.filepath = Path(self.data_dir) / filename

    def update_sensor_data(self, data):

        if self.filepath is None:
            raise Exception("Training log has not been initialized")
        logging.debug(f"Writing to {self.filepath}:\t{data}")

        # if 'vehicle_ctl' not in data or \
        #    'camera' not in data:
        #     return
