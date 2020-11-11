
class Command(object):
    """
    Command class used to set vehicle settings
    """

    def __init__(self):

        self.heading = 0.0
        self.throttle = 0.0

    def get_heading(self):
        return self.heading

    def get_throttle(self):
        return self.throttle

    def set_heading(self, heading):

        self.check_bounds(heading, "heading", -1.0, 1.0)
        self.heading = heading

    def set_throttle(self, throttle):

        self.check_bounds(throttle, "throttle", -1.0, 1.0)
        self.throttle = throttle

    def check_bounds(self, value, value_name, min_value, max_value):

        if value < min_value or value > max_value:
            raise Exception(f"{value_name} outside bounds")

    def to_json(self):

        json_cmd = {
            'throttle': self.throttle,
            'heading': self.heading,
        }

        return json_cmd

    def from_json(self, json_cmd):

        if 'throttle' not in json_cmd:
            raise Exception("No throttle command in json")
        self.set_throttle(json_cmd['throttle'])

        if 'heading' not in json_cmd:
            raise Exception("No heading command in json")
        self.set_heading(json_cmd['heading'])
