# Rotor.ai Command Line ESC Interface
# Copyright 2020 Robbie and Stu
import time
from signal import pause

import logging
from gpiozero import PWMLED, Servo, LED
from gpiozero.pins.rpigpio import RPiGPIOFactory
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero.pins.native import NativeFactory

pigpiofactory = PiGPIOFactory('localhost', 8888)

from constants import Constants
from motor import Motor
from steeringwheel import SteeringWheel
from vehiclelight import VehicleLight

motorPeriod_ms = 20   #unit in milliseconds

logger = logging.getLogger()
head_lights = VehicleLight(logger, PWMLED(Constants.GPIO_PIN_HEADLIGHTS))
fog_lights = VehicleLight(logger, PWMLED(Constants.GPIO_PIN_FOGLIGHTS))
turn_signal_left = VehicleLight(logger, PWMLED(Constants.GPIO_PIN_LEFT_TURNSIGNAL))
turn_signal_right = VehicleLight(logger, PWMLED(Constants.GPIO_PIN_RIGHT_TURNSIGNAL))
reverse_lights = VehicleLight(logger, PWMLED(Constants.GPIO_PIN_REVERSE_LIGHTS))
tail_light_left = VehicleLight(logger, PWMLED(Constants.GPIO_PIN_LEFT_TAILLIGHT))
tail_light_right = VehicleLight(logger, PWMLED(Constants.GPIO_PIN_RIGHT_TAILLIGHT))


steeringWheel = SteeringWheel(logger, Servo(Constants.GPIO_PIN_STEERING_SERVO))
min_pulse = 1/1000
max_pulse = 2/1000
motor = Motor(Servo(Constants.GPIO_PIN_ELECTRONIC_SPEED_CONTROLLER, min_pulse_width=min_pulse, max_pulse_width=max_pulse , frame_width=motorPeriod_ms/1000, pin_factory=pigpiofactory))

lights = [head_lights, fog_lights,turn_signal_left, turn_signal_right, reverse_lights, tail_light_left, tail_light_right]

print("Giving time for the ESC to calibrate...")
time.sleep(4)

throttle_delay = 100000000

nextIncrementTime = time.time_ns() + throttle_delay
currentValue = 0
waxwane = 1


while True:

    if (time.time_ns() > nextIncrementTime):
        currentValue += 1 * waxwane

        if (currentValue > 50):
            currentValue = 50
            waxwane *= -1
        if (currentValue < -50):
            currentValue = -50
            waxwane *= -1

        if (currentValue == 0):
            motor.set_throttle('N000')
            print('N000')
            time.sleep(1)
            if (waxwane == -1):
                print("fake reverse for a moment...")
                #https://www.youtube.com/watch?v=FzbJ8yVIm_c
                #Thank you  GrandadIsAnOldMan!
                motor.set_throttle('R020')
                time.sleep(0.04)
                motor.set_throttle('N000')
        # if abs(currentValue) < 40:
        #     cmd = 'N000'
        elif currentValue < 0:
            cmd = 'R' + str(format(abs(currentValue), '0>3'))
        else:
            cmd = 'F' + str(format(abs(currentValue), '0>3'))
        motor.set_throttle(cmd)
        print(cmd + ' ' + str(motor.servo_ref.value))
        nextIncrementTime = time.time_ns() + throttle_delay
