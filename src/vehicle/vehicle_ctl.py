from common.command import Command
import threading
import time
import logging
from vehicle.throttle import Throttle
from vehicle.heading import Heading
import os


class CommandThread(threading.Thread):
    """ Main thread for the vehicle controller """

    def __init__(self, *args, **kwargs):
        super(CommandThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self.command = Command()

        # Flag noting whether this is the vehicle or if it's a test server
        self.is_vehicle = False
        if 'VEHICLE' in os.environ:
            self.is_vehicle = True

        if self.is_vehicle:
            self.throttle = Throttle()
            self.heading = Heading()

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
            self.heading.update_command(command)


class VehicleCtl(object):
    """ Control class for the vehicle """

    def __init__(self):
        self.thread = CommandThread()

    def get_cmd(self):
        with self.thread.lock:
            return self.thread.command

    def set_cmd(self, command):
        with self.thread.lock:
            logging.debug(f"Received new command: {command.to_json()}")
            self.thread.command = command

    def run(self):
        self.thread.start()

    def stop(self):
        self.thread.stop()
        self.thread.join()


if __name__ == '__main__':

    try:

        vehicle_ctl = VehicleCtl()
        vehicle_ctl.run()
        time.sleep(2)
        cmd = Command()
        cmd.throttle = 1.0
        vehicle_ctl.set_cmd(cmd)
        time.sleep(2)
        vehicle_ctl.stop()

    except KeyboardInterrupt:
        vehicle_ctl.stop()


