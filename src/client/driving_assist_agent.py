import logging
from common.config_handler import ConfigHandler


class DrivingAssistAgent(object):

    def __init__(self):
        self.config_handler = ConfigHandler.get_instance()
        self.distance_threshold = self.config_handler.get_config_value_or('distance_threshold', 100)
        self.current_distance = 0.0

    def update_sensor_data(self, data):

        if 'distance_sensor' not in data:
            return
        distance_data = data['distance_sensor']

        if 'distance' not in distance_data:
            return
        self.current_distance = distance_data['distance']

    def get_assisted_command(self, command):

        # Check if we're under the distance threshold, in which case we set the throttle to zero
        if self.current_distance < self.distance_threshold and command.get_throttle() > 0.0:
            logging.info("Sensor distance below threshold, stopping the vehicle")
            command.set_throttle(0)

        return command
