from common.command import Command
from common.config_handler import ConfigHandler
from ai.simple_net import SimpleNet
from torch.utils.data import DataLoader
from ai.single_image_dataset import SingleImageDataset
import threading
import time
import logging
from pathlib import Path
import torch
from ai.label import Label


class ProcessingThread(threading.Thread):
    """
    Main processing thread for the autonomous agent
    """

    def __init__(self, *args, **kwargs):
        super(ProcessingThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self._processing_event = threading.Event()

        self._lock = threading.Lock()
        self._command = Command()
        self._data = {}

        self._config_handler = ConfigHandler.get_instance()
        self._data_dir = self._config_handler.get_config_value_or('data_dir', '/data')

        self._model = SimpleNet()
        model_path = Path(self._config_handler.get_rotor_dir()) / Path('src/nn_model.pt')
        self._model.load_state_dict(torch.load(model_path))

        # Set the model into evaluation mode
        self._model.eval()

        self._dataset = SingleImageDataset()

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
        with self._lock:
            self._data = data

    def get_command(self):
        with self._lock:
            return self._command

    def processing(self):
        return self._processing_event.is_set()

    def run(self):
        while not self.stopped():

            if self.processing():

                data = {}
                with self._lock:
                    data = self._data

                command = self.process_data(data)

                with self._lock:
                    self._command = command

            time.sleep(.05)

    def process_data(self, data) -> Command:

        ret_command = Command()
        ret_command.set_throttle(self.generate_throttle(data))
        ret_command.set_steering(self.generate_steering(data))

        return ret_command

    def generate_throttle(self, data) -> float:

        if 'distance_sensor' in data:
            distance_data = data['distance_sensor']
            if 'distance' in distance_data:
                distance = distance_data['distance']
                if distance < 50:
                    return 0.0

        return 1.0

    def generate_steering(self, data) -> float:

        if 'camera' in data:
            camera_data = data['camera']
            if 'filename' in camera_data:
                filename = camera_data['filename']
                filepath = Path(self._data_dir) / Path(filename)

                # Load the image into the dataset
                self._dataset.load_image(filepath)

                # Create a data loader for the updated dataset
                data_loader = DataLoader(self._dataset, batch_size=1)
                data_iter = iter(data_loader)
                image = data_iter.next()

                # Generate the steering value prediction
                output = self._model(image)
                _, label_index = torch.max(output, dim=1)

                logging.info(f"Steering prediction: {Label.label_index_to_name(label_index)}")
                return Label.label_index_to_steering_value(label_index)

        return 0.0


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
