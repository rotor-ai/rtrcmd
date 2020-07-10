# Rotor.ai Command Line ESC Interface
# Copyright 2020 Robbie and Stu
import time

from gpiozero import PWMLED, Servo

from constants import Constants
from motor import Motor
from steeringwheel import SteeringWheel
from vehiclelight import VehicleLight

head_lights = VehicleLight(PWMLED(Constants.GPIO_PIN_HEADLIGHTS))
fog_lights = VehicleLight(PWMLED(Constants.GPIO_PIN_FOGLIGHTS))
turn_signal_left = VehicleLight(PWMLED(Constants.GPIO_PIN_LEFT_TURNSIGNAL))
turn_signal_right = VehicleLight(PWMLED(Constants.GPIO_PIN_RIGHT_TURNSIGNAL))
reverse_lights = VehicleLight(PWMLED(Constants.GPIO_PIN_REVERSE_LIGHTS))
tail_light_left = VehicleLight(PWMLED(Constants.GPIO_PIN_LEFT_TAILLIGHT))
tail_light_right = VehicleLight(PWMLED(Constants.GPIO_PIN_RIGHT_TAILLIGHT))

steeringWheel = SteeringWheel(Servo(Constants.GPIO_PIN_STEERING_SERVO))
motor = Motor(Servo(Constants.GPIO_PIN_ELECTRONIC_SPEED_CONTROLLER))

items = [head_lights, fog_lights,turn_signal_left, turn_signal_right, reverse_lights, tail_light_left, tail_light_right, steeringWheel, motor]


#head_lights.start_blinking()
# turn_signal_left.start_blinking()
# turn_signal_right.start_blinking()
#tail_light_left.start_blinking()
# tail_light_right.start_blinking()
# reverse_lights.start_blinking()
fog_lights.start_blinking()
while True:
    for item in items:
        item.update()


