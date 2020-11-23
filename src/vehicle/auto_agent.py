from common.command import Command
import threading
import time
import logging


class ProcessingThread(threading.Thread):
    """
    Main processing thread for the autonomous agent
    """

    def __init__(self, *args, **kwargs):
        super(ProcessingThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self._processing_event = threading.Event()

        self.lock = threading.Lock()
        self.command = Command()
        self.data = {}

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def set_processing(self, processing):
        if processing:
            logging.info("Beginning processing on autonomous agent")
            self._processing_event.set()
        else:
            logging.info("Stopping processing on autonomous agent")
            self._processing_event.clear()

    def set_data(self, data):
        with self.lock:
            self.data = data

    def get_command(self):
        with self.lock:
            return self.command

    def processing(self):
        return self._processing_event.is_set()

    def run(self):
        while not self.stopped():

            if self.processing():

                data = {}
                with self.lock:
                    data = self.data

                command = self.process_data(data)

                with self.lock:
                    self.command = command

            time.sleep(1)

    def process_data(self, data) -> Command:

        # This is where we actually process data and return a command
        return Command()


class AutoAgent(object):

    def __init__(self):
        self.thread = ProcessingThread()

    def update_sensor_data(self, data):
        self.thread.set_data(data)

    def get_command(self):
        return self.thread.get_command()

    def start(self):
        self.thread.start()

    def running(self):
        return not self.thread.stopped()

    def set_processing(self, processing):
        self.thread.set_processing(processing)

    def stop(self):
        self.thread.stop()
        self.thread.join()
