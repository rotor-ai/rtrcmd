from vehicle.vehicle_sensor import VehicleSensor
from common.config_handler import ConfigHandler
import time
import threading
import logging

# Surround this in a try/except so it can be run on a non-pi machine
try:
    import RPi.GPIO as GPIO
except ImportError:
    pass


class SensorThread(threading.Thread):

    def __init__(self, *args, **kwargs):
        super(SensorThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self.distance = 0
        self.config_handler = ConfigHandler.get_instance()
        self.trigger_pin = self.config_handler.get_config_value_or('trigger_pin', 23)
        self.echo_pin = self.config_handler.get_config_value_or('echo_pin', 24)

        self.lock = threading.Lock()
        self.loop_delay = 0.05
        self.timeout = 0.5

        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def get_distance(self):
        with self.lock:
            return self.distance

    def run(self):

        logging.info("Warming up distance sensor")
        GPIO.output(self.trigger_pin, False)
        time.sleep(.5)

        while True:
            if self.stopped():
                return

            # Send the trigger high for a short time to trigger a distance measurement
            GPIO.output(self.trigger_pin, True)
            time.sleep(0.00001)
            GPIO.output(self.trigger_pin, False)

            # Wait for the echo signal to go high, or it to time out if it never goes high
            start_time = time.time()
            pulse_start = start_time
            while GPIO.input(self.echo_pin) == 0:

                # Check if we timed out
                if (pulse_start - start_time) > self.timeout:
                    return

                pulse_start = time.time()

            # Wait for the echo signal to go low, or it to time out if it never goes low
            start_time = time.time()
            pulse_end = start_time
            while GPIO.input(self.echo_pin) == 1:

                # Check if we timed out
                if (pulse_end - start_time) > self.timeout:
                    return

                pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150  # Speed of sound in cm/s divided by 2 for there and back
            distance = round(distance, 2)

            with self.lock:
                self.distance = distance

            time.sleep(self.loop_delay)


class DistanceSensor(VehicleSensor):

    def __init__(self):
        self.sensor_thread = SensorThread()

    def get_data(self) -> dict:
        return {'distance': self.sensor_thread.get_distance()}

    def start(self):
        self.sensor_thread.start()

    def stop(self):
        self.sensor_thread.stop()
        self.sensor_thread.join()
