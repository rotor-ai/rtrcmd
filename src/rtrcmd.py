# Rotor.ai Command Line ESC Interface
# Copyright 2020 Robbie and Stu
import time

from gpiozero import PWMLED, Servo

from constants import Constants
from motor import Motor
from steeringwheel import SteeringWheel
from vehiclelight import VehicleLight

motorPeriod_ms = 19.8   #unit in milliseconds
minDuty_pct = 4.5    #unit in percentage
maxDuty_pct = 10.5   #unit in percentage

head_lights = VehicleLight(PWMLED(Constants.GPIO_PIN_HEADLIGHTS))
fog_lights = VehicleLight(PWMLED(Constants.GPIO_PIN_FOGLIGHTS))
turn_signal_left = VehicleLight(PWMLED(Constants.GPIO_PIN_LEFT_TURNSIGNAL))
turn_signal_right = VehicleLight(PWMLED(Constants.GPIO_PIN_RIGHT_TURNSIGNAL))
reverse_lights = VehicleLight(PWMLED(Constants.GPIO_PIN_REVERSE_LIGHTS))
tail_light_left = VehicleLight(PWMLED(Constants.GPIO_PIN_LEFT_TAILLIGHT))
tail_light_right = VehicleLight(PWMLED(Constants.GPIO_PIN_RIGHT_TAILLIGHT))

steeringWheel = SteeringWheel(Servo(Constants.GPIO_PIN_STEERING_SERVO))
min_pulse = ((minDuty_pct*0.01)*motorPeriod_ms)/1000
max_pulse = ((maxDuty_pct*0.01)*motorPeriod_ms)/1000
motor = Motor(Servo(Constants.GPIO_PIN_ELECTRONIC_SPEED_CONTROLLER, min_pulse_width=min_pulse, max_pulse_width=max_pulse , frame_width=motorPeriod_ms/1000))

lights = [head_lights, fog_lights,turn_signal_left, turn_signal_right, reverse_lights, tail_light_left, tail_light_right]

throttle_delay = 0.15


for i in range(0, 100, 2):
    cmd = 'F'+ str(format(i, '0>3'))
    print(cmd)
    motor.set_throttle(cmd)
    time.sleep(throttle_delay)

for i in range(100, 0, -2):
    cmd = 'F'+ str(format(i, '0>3'))
    print(cmd)
    motor.set_throttle(cmd)
    time.sleep(throttle_delay)

motor.set_throttle('N000')
time.sleep(3)

for i in range(0, 100, 2):
    cmd = 'R'+ str(format(i, '0>3'))
    print(cmd)
    motor.set_throttle(cmd)
    time.sleep(throttle_delay)

for i in range(100, 0, -2):
    cmd = 'R'+ str(format(i, '0>3'))
    print(cmd)
    motor.set_throttle(cmd)
    time.sleep(throttle_delay)

