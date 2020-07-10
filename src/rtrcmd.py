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

lights = [head_lights, fog_lights,turn_signal_left, turn_signal_right, reverse_lights, tail_light_left, tail_light_right]

time_to_shift_to_next_item = time.time() + 2
active_item = 0
lights[active_item].start_blinking()

while True:
    for light in lights:
        light.update()

    if (time.time() > time_to_shift_to_next_item):
        time_to_shift_to_next_item = time.time() + 2
        lights[active_item].set_off()
        lights[active_item].blinking = False
        active_item = (active_item + 1) % len(lights)
        lights[active_item].start_blinking()

