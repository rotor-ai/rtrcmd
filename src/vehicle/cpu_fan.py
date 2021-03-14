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
        if self.fanState == 1 and current_temp <= 35:
            self.fanState = False
            print("turning fan off")
            self.fan.value = self.fanState
            print("CPU is " + str(current_temp) + "C   Fan state is " + str(self.fan.value))
        elif self.fanState == 0 and current_temp >= 40:
            self.fanState = True
            print("turning fan on")
            self.fan.value = self.fanState
            print("CPU is " + str(current_temp) + "C   Fan state is " + str(self.fan.value))

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
