# Rotor.ai Command Line ESC Interface
# Copyright 2020 Robbie and Stu
import time

from gpiozero import PWMLED, Servo

from constants import Constants
from motor import Motor
from steeringwheel import SteeringWheel
from vehiclelight import VehicleLight

headlights = VehicleLight(PWMLED(Constants.GPIO_PIN_HEADLIGHTS))
driverSideTailLight = VehicleLight(PWMLED(Constants.GPIO_PIN_LEFT_TAILLIGHT))
passengerSideTailLight = VehicleLight(PWMLED(Constants.GPIO_PIN_RIGHT_TAILLIGHT))
steeringWheel = SteeringWheel(Servo(Constants.GPIO_PIN_STEERING_SERVO))
motor = Motor(Servo(Constants.GPIO_PIN_ELECTRONIC_SPEED_CONTROLLER))

items = [headlights, driverSideTailLight, passengerSideTailLight, steeringWheel, motor]

headlights.set_off()
driverSideTailLight.set_off()
steeringWheel.set_heading('N000')
motor.set_throttle('N000')
time.sleep(1)
steeringWheel.set_heading('L100')
time.sleep(1)
steeringWheel.set_heading('R100')
time.sleep(1)
steeringWheel.set_heading('N000')
time.sleep(1)
motor.set_throttle('F100')
time.sleep(5)
motor.servo_ref.setOff()
motor.set_throttle('N000')
time.sleep(5)
motor.set_throttle('R100')
time.sleep(5)
motor.set_throttle('N000')

