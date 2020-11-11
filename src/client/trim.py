
class Trim(object):
    """
    Command class used to set vehicle settings
    """

    def __init__(self):

        # Heading trim
        self.heading_trim = 0.0
        self.heading_max = 1.0
        self.heading_min = -1.0

        # Throttle trim
        self.throttle_fwd_min = 0.0
        self.throttle_fwd_max = 1.0
        self.throttle_rev_min = 0.0
        self.throttle_rev_max = -1.0

    def get_heading_trim(self):
        return self.heading_trim

    def get_heading_max(self):
        return self.heading_max

    def get_heading_min(self):
        return self.heading_min

    def get_throttle_fwd_min(self):
        return self.throttle_fwd_min

    def get_throttle_fwd_max(self):
        return self.throttle_fwd_max

    def get_throttle_rev_min(self):
        return self.throttle_rev_min

    def get_throttle_rev_max(self):
        return self.throttle_rev_max

    def set_heading_trim(self, heading_trim):

        self.check_bounds(heading_trim, "heading trim", -1.0, 1.0)
        self.heading_trim = heading_trim

    def set_heading_max(self, heading_max):

        self.check_bounds(heading_max, "heading max", 0.0, 1.0)
        self.heading_max = heading_max

    def set_heading_min(self, heading_min):

        self.check_bounds(heading_min, "heading min", -1.0, 0.0)
        self.heading_min = heading_min

    def set_throttle_fwd_max(self, throttle_fwd_max):

        self.check_bounds(throttle_fwd_max, "throttle fwd max", 0.0, 1.0)
        self.throttle_fwd_max = throttle_fwd_max

    def set_throttle_fwd_min(self, throttle_fwd_min):

        self.check_bounds(throttle_fwd_min, "throttle fwd min", 0.0, 1.0)
        self.throttle_fwd_min = throttle_fwd_min

    def set_throttle_rev_max(self, throttle_rev_max):

        self.check_bounds(throttle_rev_max, "throttle rev max", -1.0, 0.0)
        self.throttle_rev_max = throttle_rev_max

    def set_throttle_rev_min(self, throttle_rev_min):

        self.check_bounds(throttle_rev_min, "throttle fwd min", -1.0, 0.0)
        self.throttle_rev_min = throttle_rev_min

    def check_bounds(self, value, value_name, min_value, max_value):

        if value < min_value or value > max_value:
            raise Exception(f"{value_name} outside bounds")

    def get_trimmed_throttle(self, throttle):

        trimmed_throttle = throttle
        if 0.0 < trimmed_throttle < self.throttle_fwd_min:
            trimmed_throttle = self.throttle_fwd_min
        elif trimmed_throttle > self.throttle_fwd_max:
            trimmed_throttle = self.throttle_fwd_max
        elif self.throttle_rev_min < trimmed_throttle < 0.0:
            trimmed_throttle = self.throttle_rev_min
        elif trimmed_throttle < self.throttle_rev_max:
            trimmed_throttle = self.throttle_rev_max

        return trimmed_throttle

    def get_trimmed_heading(self, heading):

        trimmed_heading = heading + self.heading_trim
        if trimmed_heading > self.heading_max:
            trimmed_heading = self.heading_max
        elif trimmed_heading < self.heading_min:
            trimmed_heading = self.heading_min

        return trimmed_heading

    def to_json(self):

        json_cmd = {
            'heading_trim': self.heading_trim,
            'heading_max': self.heading_max,
            'heading_min': self.heading_min,
            'throttle_fwd_max': self.throttle_fwd_max,
            'throttle_fwd_min': self.throttle_fwd_min,
            'throttle_rev_max': self.throttle_rev_max,
            'throttle_rev_min': self.throttle_rev_min
        }

        return json_cmd

    def from_json(self, json_cmd):

        if 'heading_trim' in json_cmd:
            self.set_heading_trim(json_cmd['heading_trim'])
        if 'heading_max' in json_cmd:
            self.set_heading_max(json_cmd['heading_max'])
        if 'heading_min' in json_cmd:
            self.set_heading_min(json_cmd['heading_min'])
        if 'throttle_fwd_max' in json_cmd:
            self.set_throttle_fwd_max(json_cmd['throttle_fwd_max'])
        if 'throttle_fwd_min' in json_cmd:
            self.set_throttle_fwd_min(json_cmd['throttle_fwd_min'])
        if 'throttle_rev_max' in json_cmd:
            self.set_throttle_rev_max(json_cmd['throttle_rev_max'])
        if 'throttle_rev_min' in json_cmd:
            self.set_throttle_rev_min(json_cmd['throttle_rev_min'])
