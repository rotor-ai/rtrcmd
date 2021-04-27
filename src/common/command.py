
class Command(object):
    """
    Command class used to set vehicle settings
    """

    def __init__(self, s=0.0, t=0.0):
        self.set_steering(s)
        self.set_throttle(t)

    def get_steering(self):
        return self.steering

    def get_throttle(self):
        return self.throttle

    def set_steering(self, steering):

        self.check_bounds(steering, "steering", -1.0, 1.0)
        self.steering = steering

    def set_throttle(self, throttle):

        self.check_bounds(throttle, "throttle", -1.0, 1.0)
        self.throttle = throttle

    def check_bounds(self, value, value_name, min_value, max_value):

        if value < min_value or value > max_value:
            raise Exception(f"{value_name} outside bounds")

    def to_json(self):

        json_cmd = {
            'throttle': self.throttle,
            'steering': self.steering,
        }

        return json_cmd

    def equal(self, some_other_command):
        return self.to_json() == some_other_command.to_json()

    def from_json(self, json_cmd):

        if 'throttle' not in json_cmd:
            raise Exception("No throttle command in json")
        self.set_throttle(json_cmd['throttle'])

        if 'steering' not in json_cmd:
            raise Exception("No steering command in json")
        self.set_steering(json_cmd['steering'])
