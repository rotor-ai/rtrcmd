
class Command(object):
    """ Command class used to set vehicle settings """

    def __init__(self):
        self.throttle = 0.0
        self.heading = 0.0

    def get_throttle(self):
        return self.throttle

    def get_heading(self):
        return self.heading

    def set_throttle(self, throttle):

        if throttle > 1.0 or throttle < -1.0:
            raise Exception("Throttle value outside bounds")
        self.throttle = throttle

    def set_heading(self, heading):

        if heading > 1.0 or heading < -1.0:
            raise Exception("Heading value outside bounds")
        self.heading = heading

    def to_json(self):

        json_cmd = {
            'throttle': self.throttle,
            'heading': self.heading
        }

        return json_cmd

    def from_json(self, json_cmd):

        if 'throttle' not in json_cmd:
            raise Exception("No throttle command in json")
        self.set_throttle(json_cmd['throttle'])

        if 'heading' not in json_cmd:
            raise Exception("No heading command in json")
        self.set_heading(json_cmd['heading'])
