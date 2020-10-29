from command import Command
import threading
import time
import logging
from throttle import Throttle
from heading import Heading


class CommandThread(threading.Thread):
    """ Main thread for the vehicle controller """

    def __init__(self, *args, **kwargs):
        super(CommandThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self.command = Command()

        self.is_vehicle = False  # Flag to set for testing, TODO: Figure out a better way to do this
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
            self.throttle.set_throttle(command.get_throttle())
            self.heading.set_heading(command.get_heading())


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


