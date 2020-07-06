# Rotor.ai Command Line ESC Interface
# Copyright 2020 Robbie and Stu

from gpiozero import PWMLED, Servo

from constants import Constants
from steeringwheel import SteeringWheel
from vehiclelight import VehicleLight

headlights = VehicleLight(PWMLED(Constants.GPIO_PIN_HEADLIGHTS))
driverSideTailLight = VehicleLight(PWMLED(Constants.GPIO_PIN_LEFT_TAILLIGHT))
passengerSideTailLight = VehicleLight(PWMLED(Constants.GPIO_PIN_RIGHT_TAILLIGHT))
steeringWheel = SteeringWheel(Servo(Constants.GPIO_PIN_STEERING_SERVO))

items = [headlights, driverSideTailLight, passengerSideTailLight, steeringWheel]

headlights.set_bright()
driverSideTailLight.start_blinking()
passengerSideTailLight.start_blinking()


while True:

	for item in items:
		item.update()

