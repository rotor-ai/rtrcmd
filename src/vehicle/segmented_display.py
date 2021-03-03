import adafruit_ht16k33.segments


class SegmentedDisplay:

    def __init__(self, i_square_c_instance):
        self.segmentDisplayInstance = adafruit_ht16k33.segments.Seg7x4(i_square_c_instance)

    def set_text(self, text):
        self.segmentDisplayInstance.fill(0)
        self.segmentDisplayInstance.print(text)