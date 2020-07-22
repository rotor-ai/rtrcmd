# Rotor.ai Command Line ESC Interface
# Copyright 2020 Robbie and Stu
import time

from gpiozero import PWMLED, Servo, Device
from gpiozero.pins.rpigpio import RPiGPIOFactory
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero.pins.native import NativeFactory


from constants import Constants
from motor import Motor
from steeringwheel import SteeringWheel
from vehiclelight import VehicleLight

motorPeriod_ms = 20   #unit in milliseconds
minDuty_pct = 5    #unit in percentage
maxDuty_pct = 10   #unit in percentage

# head_lights = VehicleLight(PWMLED(Constants.GPIO_PIN_HEADLIGHTS))
# fog_lights = VehicleLight(PWMLED(Constants.GPIO_PIN_FOGLIGHTS))
# turn_signal_left = VehicleLight(PWMLED(Constants.GPIO_PIN_LEFT_TURNSIGNAL))
# turn_signal_right = VehicleLight(PWMLED(Constants.GPIO_PIN_RIGHT_TURNSIGNAL))
# reverse_lights = VehicleLight(PWMLED(Constants.GPIO_PIN_REVERSE_LIGHTS))
# tail_light_left = VehicleLight(PWMLED(Constants.GPIO_PIN_LEFT_TAILLIGHT))
# tail_light_right = VehicleLight(PWMLED(Constants.GPIO_PIN_RIGHT_TAILLIGHT))

# steeringWheel = SteeringWheel(Servo(Constants.GPIO_PIN_STEERING_SERVO))
min_pulse = 1/1000
max_pulse = 2/1000
motor = Motor(Servo(Constants.GPIO_PIN_ELECTRONIC_SPEED_CONTROLLER, min_pulse_width=min_pulse, max_pulse_width=max_pulse , frame_width=motorPeriod_ms/1000))

# lights = [head_lights, fog_lights,turn_signal_left, turn_signal_right, reverse_lights, tail_light_left, tail_light_right]

throttle_delay = 0.1
throttle_increment = 1
print("waiting for ESC to calibrate...")
time.sleep(4)

while True:

    for i in range(0, 100, throttle_increment):
        cmd = 'F'+ str(format(i, '0>3'))
        print(cmd)
        motor.set_throttle(cmd)
        time.sleep(throttle_delay)

    # pause()

    for i in range(100, 0, -1*throttle_increment):
        cmd = 'F'+ str(format(i, '0>3'))
        print(cmd)
        motor.set_throttle(cmd)
        time.sleep(throttle_delay)

    motor.set_throttle('N000')
    time.sleep(2)

    for i in range(0, 101, throttle_increment):
        cmd = 'R'+ str(format(i, '0>3'))
        print(cmd)
        motor.set_throttle(cmd)
        time.sleep(throttle_delay)

    for i in range(100, 0, -1*throttle_increment):
        cmd = 'R'+ str(format(i, '0>3'))
        print(cmd)
        motor.set_throttle(cmd)
        time.sleep(throttle_delay)

    motor.set_throttle('N000')
    time.sleep(2)