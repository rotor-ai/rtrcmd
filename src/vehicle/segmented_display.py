import threading
import time
import adafruit_ht16k33.segments
import netifaces


class SegmentedDisplay(threading.Thread):

    def __init__(self, i_square_c_instance):
        super().__init__()
        self.segmentDisplayInstance = adafruit_ht16k33.segments.Seg7x4(i_square_c_instance)
        self.loop_delay = 1
        self.runDuration = 0

    def set_text(self, text):
        self.segmentDisplayInstance.fill(0)
        self.segmentDisplayInstance.print(text)

    def run(self) -> None:
        super().run()
        while 1:
            time.sleep(self.loop_delay)
            self.runDuration += self.loop_delay

            ipaddress = "    " + netifaces.ifaddresses('wlan0')[2][0]['addr']
            position = self.runDuration % len(ipaddress)
            scrolling_ip_address = ipaddress[position:] + ipaddress[:position]
            self.set_text(scrolling_ip_address)

