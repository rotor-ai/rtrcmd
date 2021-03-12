from common.command import Command
from common.trim import Trim
import threading
import time
import logging
from .vehicle_sensor import VehicleSensor
from common.config_handler import ConfigHandler

# Surround the import in a try/catch to accommodate running on non-vehicles
try:
    from .throttle import Throttle
    from .steering import Steering
except ModuleNotFoundError as e:
    logging.error(e)
    pass


class CommandThread(threading.Thread):
    """ Main thread for the vehicle controller """

    def __init__(self, *args, **kwargs):
        super(CommandThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self.command = Command()
        self.config_handler = ConfigHandler.get_instance()

        # Flag noting whether this is the vehicle or if it's a test server
        self.is_vehicle = self.config_handler.get_config_value_or('is_vehicle', True)

        # Pull in the trim from the config file
        self.trim = Trim()
        self.trim.from_json(self.config_handler.get_config_value_or('trim', {}))

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

            with self.lock:
                self.execute_command()

            time.sleep(self.loop_delay)

    def execute_command(self):

        if self.is_vehicle:

            # Calculate trimmed values and update
            trimmed_throttle = self.trim.get_trimmed_throttle(self.command.get_throttle())
            trimmed_steering = self.trim.get_trimmed_steering(self.command.get_steering())

            self.throttle.update_throttle(trimmed_throttle)
            self.steering.update_steering(trimmed_steering)


class CmdCtl(VehicleSensor):
    """
    Command and control class for the vehicle. Implements VehicleSensor because we want to be able to pull the current
    command which is dumped into the rest of the sensor data.
    """

    def __init__(self):
        self.thread = CommandThread()

    def get_cmd(self):
        with self.thread.lock:
            return self.thread.command

    def get_data(self) -> dict:
        return {'command': self.get_cmd().to_json()}

    def set_cmd(self, command):
        with self.thread.lock:
            logging.debug(f"Received new command: {command.to_json()}")
            self.thread.command = command

    def get_trim(self):
        with self.thread.lock:
            return self.thread.trim

    def set_trim(self, trim):
        with self.thread.lock:
            logging.debug(f"Received new trim: {trim.to_json()}")
            self.thread.config_handler.set_config_value('trim', trim.to_json())
            self.thread.trim = trim

    def start(self):
        self.thread.start()

    def stop(self):
        self.thread.stop()
        self.thread.join()
