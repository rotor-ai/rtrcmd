from vehicle.auto_agent import AutoAgent
from vehicle.training_agent import TrainingAgent
from vehicle.driving_assist_agent import DrivingAssistAgent
from vehicle.sensor_manager import SensorManager
from common.mode import Mode, ModeType
from vehicle.vehicle_ctl import VehicleCtl
from threading import Lock
import logging
from time import sleep


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

        # Create the auto agent and start it
        self.auto_agent = AutoAgent()
        self.auto_agent.start()

        # Create the sensor manager and start it
        self.sensor_mgr = SensorManager()
        self.sensor_mgr.start_sensors()

    def poll_sensor_data(self):

        # Get the sensor data from the sensor manager
        data = self.sensor_mgr.get_sensor_data()

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

    def set_mode(self, new_mode):

        # If we're not actually changing the mode, leave
        if new_mode.get_mode() == self.mode.get_mode():
            return

        with self.lock:

            logging.info(f"Moving into mode: {new_mode.get_mode_name()}")

            # If we're moving into auto mode, turn on the auto agent
            if new_mode.get_mode() == ModeType.AUTO:
                self.auto_agent.set_processing(True)

            # If we're moving out of auto mode, turn off the auto agent
            if self.mode.get_mode() == ModeType.AUTO:
                self.auto_agent.set_processing(False)

            # Start a new log if we're switching into training mode
            if new_mode.get_mode() == ModeType.TRAIN:
                self.training_agent.init_new_log()

            # Assign the new mode
            self.mode = new_mode

    def get_mode(self):
        with self.lock:
            return self.mode

    def run_forever(self):

        while True:
            self.poll_sensor_data()
            sleep(.1)

    def stop(self):
        self.vehicle_ctl.stop()
        self.auto_agent.stop()
        self.sensor_mgr.stop_sensors()
