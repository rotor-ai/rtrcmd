from constants import Constants
from vehicledevice import VehicleDevice


class SteeringWheel(VehicleDevice):

    def __init__(self, servo):
        self.servo_ref = servo
        self.servo_ref.value = Constants.SERVO_CENTER_PWM_VALUE

    def set_heading(self, command):
        if (not len(command)==4):
            return

        if (command[0] == 'L'):
            servo_limit = 1
        elif(command[0] == 'R'):
            servo_limit = -1
        elif(command[0] == 'N'):
            self.servo_ref.value = Constants.SERVO_CENTER_PWM_VALUE
            return
        else:
            return

        magnitude = int(command[1:])
        servo_direction_range = servo_limit - Constants.SERVO_CENTER_PWM_VALUE
        interpolated_value = ((magnitude)/100) * servo_direction_range + Constants.SERVO_CENTER_PWM_VALUE
        self.servo_ref.value = interpolated_value

    def update(self):
        pass
