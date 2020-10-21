import json

"""
Command class used to set vehicle settings
"""
class Command(object):

    def __init__(self):
        self.throttle = 0.0
        self.heading = 0.0

    def set_throttle(self, throttle):

        if throttle > 1.0 or throttle < -1.0:
            raise Exception("Throttle value outside bounds")
        self.throttle = throttle

    def set_heading(self, heading):

        if heading > 1.0 or heading < -1.0:
            raise Exception("Heading value outside bounds")
        self.heading = heading

    def to_json_string(self):

        json_command = {
            'throttle' : self.throttle,
            'heading' : self.heading
        }

        return json.dumps(json_command)

    def load_json_string(self, json_string):

        json_command = json.loads(json_string)

        if json_command['throttle'] is None:
            raise Exception("No throttle command in json")
        self.set_throttle(json_command['throttle'])

        if json_command['heading'] is None:
            raise Exception("No heading command in json")
        self.set_heading(json_command['heading'])
