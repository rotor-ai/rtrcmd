from gpiozero import Servo
import logging
from common.config_handler import ConfigHandler

from vehicle.constants import Constants


class Throttle(object):

    def __init__(self):
        self.throttle = 0.0
        self.config_handler = ConfigHandler.get_instance()

        # Get the config value, then re-write it to the config. We do this so in the case that there is no config file
        # yet, it will create one with the default value
        speed_control_pin = self.config_handler.get_config_value_or('speed_control_pin', Constants.GPIO_PIN_ELECTRONIC_SPEED_CONTROLLER)
        self.config_handler.set_config_value('speed_control_pin', speed_control_pin)
        self.servo = Servo(speed_control_pin)

    def update_throttle(self, throttle):

        if throttle == self.throttle:
            return

        # Set the new throttle
        self.throttle = throttle
        # logging.debug(f"Setting throttle to {self.throttle}")
        self.servo.value = self.throttle
