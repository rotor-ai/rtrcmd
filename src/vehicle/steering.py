from gpiozero import Servo
import logging
from common.command import Command
from common.config_handler import ConfigHandler

from vehicle.constants import Constants


class Steering(object):

    def __init__(self):
        self.steering = 0.0
        self.config_handler = ConfigHandler.get_instance()

        # Get the config value, then re-write it to the config. We do this so in the case that there is no config file
        # yet, it will create one with the default value
        steering_pin = self.config_handler.get_config_value_or('steering_pin', Constants.GPIO_PIN_STEERING_SERVO)
        self.config_handler.set_config_value('steering_pin', steering_pin)
        self.servo = Servo(steering_pin)

    def update_steering(self, steering):

        # If this is not a new command, ignore it
        if steering == self.steering:
            return

        # Set the new steering
        self.steering = steering
        # logging.debug(f"Setting steering to {self.steering}")
        self.servo.value = self.steering
