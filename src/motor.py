from constants import Constants
from vehicledevice import VehicleDevice


class Motor(VehicleDevice):

    def __init__(self, servo):
        self.servo_ref = servo
        servo.value = 0

    def set_throttle(self, command):
        if(len(command) != 4):
            return

        magnatude = int(command[1:])
        if(command[0] == 'F'):
            self.servo_ref.value = (magnatude/100) * (Constants.MOTOR_FWD_THROTTLE_MAX - Constants.MOTOR_FWD_THROTTLE_MIN) + Constants.MOTOR_FWD_THROTTLE_MIN
        elif(command[0] == 'R'):
            self.servo_ref.value = (magnatude/100) * (Constants.MOTOR_REV_THROTTLE_MAX - Constants.MOTOR_REV_THROTTLE_MIN) + Constants.MOTOR_REV_THROTTLE_MIN
        elif(command[0] == 'N'):
            self.servo_ref.value = 0.0

    def update(self):
        pass
