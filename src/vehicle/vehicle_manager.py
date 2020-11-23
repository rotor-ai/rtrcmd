from vehicle.auto_agent import AutoAgent
from vehicle.training_agent import TrainingAgent
from vehicle.driving_assist_agent import DrivingAssistAgent
from common.mode import Mode, ModeType
from vehicle.vehicle_ctl import VehicleCtl
from threading import Lock


class VehicleManager(object):
    """
    This class acts as a manager interface for controlling the vehicle. It can be used to directly control the vehicle
    or to set the current mode.
    """

    def __init__(self):

        self.training_agent = TrainingAgent()
        self.driving_assist_agent = DrivingAssistAgent()
        self.mode = Mode()

        # The mode can be set from a thread different from the one in which it was created, so this lock prevents
        # unnecessary funny business when setting the mode
        self.lock = Lock()

        # Create the vehicle controller and start it
        self.vehicle_ctl = VehicleCtl()
        self.vehicle_ctl.start()

        # Create the auto agent and start
        self.auto_agent = AutoAgent()
        self.auto_agent.start()

    def update_sensor_data(self, data):

        # Append the current user input to the data
        data['vehicle_ctl'] = self.vehicle_ctl.get_cmd().to_json()

        with self.lock:

            # If we're in autonomous mode, take the sensor data and send a new command to the vehicle controller
            if self.mode.get_mode() == ModeType.AUTO:
                self.auto_agent.update_sensor_data(data)
                command = self.auto_agent.get_command()
                self.vehicle_ctl.set_cmd(command)

            # If we're in training mode, pass the data to the trainer so it can label and save it
            elif self.mode.get_mode() == ModeType.TRAIN:
                self.training_agent.update_sensor_data(data)

            # If we're in assisted driving mode, pass the data to the assisted driving agent and allow it to update
            # the current command if needed
            elif self.mode.get_mode() == ModeType.ASSISTED:
                self.driving_assist_agent.update_sensor_data(data)
                command = self.vehicle_ctl.get_cmd()
                command = self.driving_assist_agent.get_assisted_command(command)
                self.vehicle_ctl.set_cmd(command)

    def set_command(self, command):

        # Check if we need to run it through the assisted driving command first
        with self.lock:
            if self.mode.get_mode() == ModeType.ASSISTED:
                command = self.driving_assist_agent.get_assisted_command(command)

        self.vehicle_ctl.set_cmd(command)

    def get_command(self):
        return self.vehicle_ctl.get_cmd()

    def set_trim(self, trim):
        self.vehicle_ctl.set_trim(trim)

    def get_trim(self):
        return self.vehicle_ctl.set_trim()

    def set_mode(self, mode):
        with self.lock:
            self.mode = mode

            # Toggle the auto agent on or off if necessary
            if self.mode.get_mode() == ModeType.AUTO:
                self.auto_agent.set_processing(True)
            else:
                self.auto_agent.set_processing(False)

    def get_mode(self):
        with self.lock:
            return self.mode

    def stop(self):
        self.vehicle_ctl.stop()
        self.auto_agent.stop()
