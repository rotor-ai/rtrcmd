from command import Command
import threading
import time


class CommandThread(threading.Thread):

    def __init__(self, *args, **kwargs):
        super(CommandThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self.command = Command()
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

                # TODO: Do something with the command
                pass

            time.sleep(self.loop_delay)


class VehicleCtl(object):

    def __init__(self):

        self.thread = CommandThread()

    def get_cmd(self):
        with self.thread.lock:
            return self.thread.command

    def set_cmd(self, command):
        with self.thread.lock:
            print("Setting to new command: {}".format(command.to_json()))
            self.thread.command = command

    def start(self):
        self.thread.start()

    def stop(self):
        self.thread.stop()
        self.thread.join()


if __name__ == '__main__':

    try:

        vehicle_ctl = VehicleCtl()
        vehicle_ctl.start()
        time.sleep(2)
        cmd = Command()
        cmd.throttle = 1.0
        vehicle_ctl.set_cmd(cmd)
        time.sleep(2)
        vehicle_ctl.stop()

    except KeyboardInterrupt:
        vehicle_ctl.stop()


