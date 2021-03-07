from gpiozero import Device
from gpiozero.pins.pigpio import PiGPIOFactory
from vehicle.sensor_mgr import SensorMgr
from vehicle.cmd_ctl import CmdCtl
from common.config_handler import ConfigHandler
from threading import Lock
import logging
from vehicle.image_streamer import ImageStreamer
import board
import busio as io
import netifaces

from vehicle.segmented_display import SegmentedDisplay


class VehicleMgr(object):
    """
    This class acts as a manager interface for controlling the vehicle. It can be used to directly control the vehicle
    or to set the current mode.
    """

    def __init__(self):

        self._i2c_instance = io.I2C(board.SCL, board.SDA)
        config_handler = ConfigHandler.get_instance()
        preferred_pin_factory = config_handler.get_config_value_or('preferred_pin_factory', '')
        if preferred_pin_factory == 'pigpio':
            Device.pin_factory = PiGPIOFactory()
            logging.info(f"Starting vehicle manager thread using pin factory: {Device.pin_factory}")
        else:
            logging.info("Starting vehicle manager thread using default pin factory")


        # The mode can be set from a thread different from the one in which it was created, so this lock prevents
        # unnecessary funny business when setting the mode
        self._lock = Lock()

        # Create the vehicle controller and start it
        self._vehicle_ctl = CmdCtl()
        self._vehicle_ctl.start()

        # Create the sensor manager and start it
        self._sensor_mgr = SensorMgr()
        self._sensor_mgr.start_sensors()

        #Digital Segmented display
        self._digital_display = SegmentedDisplay(self._i2c_instance)
        self._digital_display.start()
        self._digital_display.add_display_mode(mode_behavior = self.addressDisplay)

        # Create the image streamer and start it
        self._image_streamer = ImageStreamer()
        self._image_streamer.start()

    def addressDisplay(self, display):
        ipaddress = "    " + netifaces.ifaddresses('wlan0')[2][0]['addr']
        position = display.runDuration % len(ipaddress)
        scrolling_ip_address = ipaddress[position:] + ipaddress[:position]
        display.set_text(scrolling_ip_address)

    def current_telemetry(self):

        # Get the sensor data from the sensor manager
        telemetry = self._sensor_mgr.current_telemetry()

        # Append the current user input to the data
        telemetry['vehicle_ctl'] = self._vehicle_ctl.get_cmd().to_json()

        return telemetry

    def set_command(self, command):

        self._vehicle_ctl.set_cmd(command)

    def get_command(self):
        return self._vehicle_ctl.get_cmd()

    def set_trim(self, trim):
        self._vehicle_ctl.set_trim(trim)

    def get_trim(self):
        return self._vehicle_ctl.get_trim()

    def start_image_stream(self, ip, port):
        self._image_streamer.start_streaming(ip, port)

    def stop_image_stream(self):
        self._image_streamer.stop_streaming()

    def image_stream_running(self):
        return self._image_streamer.is_streaming()

    def stop(self):

        self._digital_display.stop()
        self._vehicle_ctl.stop()
        self._sensor_mgr.stop()
        self._image_streamer.stop()
