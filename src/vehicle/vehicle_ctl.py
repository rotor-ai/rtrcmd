from common.command import Command
import threading
import time
import logging
from vehicle.throttle import Throttle
from vehicle.steering import Steering
from vehicle.vehicle_sensor import VehicleSensor
from common.config_handler import ConfigHandler


class CommandThread(threading.Thread):
    """ Main thread for the vehicle controller """

    def __init__(self, *args, **kwargs):
        super(CommandThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self.command = Command()
        self.config_handler = ConfigHandler.get_instance()

        # Flag noting whether this is the vehicle or if it's a test server
        self.is_vehicle = self.config_handler.get_config_value_or('is_vehicle', False)

        if self.is_vehicle:
            self.throttle = Throttle()
            self.steering = Steering()

        self.lock = threading.Lock()
        self.loop_delay = 0.01

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):

        while True:
            if self.stopped():
                return

            command = Command()
            with self.lock:
                command = self.command

            self.execute_command(command)

            time.sleep(self.loop_delay)

    def execute_command(self, command):

        if self.is_vehicle:
            self.throttle.update_command(command)
            self.steering.update_command(command)


class VehicleCtl(VehicleSensor):
    """
    Control class for the vehicle. Implements VehicleSensor because we want to be able to pull the current command which
    is dumped into the rest of the sensor data.
    """

    def __init__(self):
        self.thread = CommandThread()

    def get_cmd(self):
        with self.thread.lock:
            return self.thread.command

    def get_data(self) -> dict:
        return {'command': self.get_cmd().to_json()}

    def get_name(self) -> str:
        return "vehicle_ctl"

    def set_cmd(self, command):
        with self.thread.lock:
            logging.debug(f"Received new command: {command.to_json()}")
            self.thread.command = command

    def run(self):
        self.thread.start()

    def stop(self):
        self.thread.stop()
        self.thread.join()
