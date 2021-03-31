import logging
import threading
import time

import gpiozero

from common.config_handler import ConfigHandler

class CpuFan():

    def __init__(self):
        self.thread = CpuFanThread()
        self.fan = gpiozero.LED(ConfigHandler.get_instance().get_config_value_or('cpu_fan_pin', 21))
        self.fan.off()
        self.fanState = False
        self.thread.behave = lambda : self.behavior()

    def behavior(self):
        current_temp = gpiozero.CPUTemperature().temperature
        if self.fanState == 1 and current_temp <= 30:
            self.fanState = False
            self.fan.value = self.fanState
            self.log_cpu_temp_and_fan_state(current_temp)
        elif self.fanState == 0 and current_temp >= 35:
            self.fanState = True
            self.fan.value = self.fanState
            self.log_cpu_temp_and_fan_state(current_temp)

    def log_cpu_temp_and_fan_state(self, current_temp):
        logging.info("CPU is " + str(current_temp) + "C   Fan state is " + str(self.fan.value))

    def start(self):
        self.thread.start()

    def stop(self):
        self.thread.stop()


class CpuFanThread(threading.Thread):

    loop_delay = 5

    def __init__(self):
        super().__init__()
        self.run_duration = 0
        self.behave = lambda : print("NO BEHAVIOR DEFINED FOR THREAD!")

    def run(self) -> None:
        super().run()
        while 1:
            self.behave()
            time.sleep(self.loop_delay)
            self.run_duration += self.loop_delay
