
class Trim(object):
    """
    Command class used to set vehicle settings
    """

    def __init__(self):

        # steering trim
        self.steering_trim = 0.0
        self.steering_max = 1.0
        self.steering_min = -1.0
        self.steering_reversed = False

        # Throttle trim
        self.throttle_trim = 0.0
        self.throttle_fwd_min = 0.0
        self.throttle_fwd_max = 1.0
        self.throttle_rev_min = 0.0
        self.throttle_rev_max = -1.0

    def get_steering_trim(self):
        return self.steering_trim

    def get_steering_reversed(self):
        return self.steering_reversed

    def get_steering_max(self):
        return self.steering_max

    def get_steering_min(self):
        return self.steering_min

    def get_throttle_trim(self):
        return self.throttle_trim

    def get_throttle_fwd_min(self):
        return self.throttle_fwd_min

    def get_throttle_fwd_max(self):
        return self.throttle_fwd_max

    def get_throttle_rev_min(self):
        return self.throttle_rev_min

    def get_throttle_rev_max(self):
        return self.throttle_rev_max

    def set_steering_trim(self, steering_trim):

        self.check_bounds(steering_trim, "steering trim", -1.0, 1.0)
        self.steering_trim = steering_trim

    def set_steering_max(self, steering_max):

        self.check_bounds(steering_max, "steering max", 0.0, 1.0)
        self.steering_max = steering_max

    def set_steering_min(self, steering_min):

        self.check_bounds(steering_min, "steering min", -1.0, 0.0)
        self.steering_min = steering_min

    def set_steering_reversed(self, reverse):

        self.steering_reversed = reverse

    def set_throttle_trim(self, throttle_trim):

        self.check_bounds(throttle_trim, "throttle trim", -1.0, 1.0)
        self.throttle_trim = throttle_trim

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

        # trimmed_throttle = throttle + self.throttle_trim
        trimmed_throttle = throttle
        if throttle > 0:
            trimmed_throttle = (self.throttle_fwd_max - self.throttle_fwd_min) * throttle + self.throttle_fwd_min
        elif throttle < 0:
            trimmed_throttle = (self.throttle_rev_min - self.throttle_rev_max) * throttle + self.throttle_rev_min
        else:
            trimmed_throttle = self.throttle_trim

        return round(trimmed_throttle, 2)

    def get_trimmed_steering(self, steering):

        if self.steering_reversed:
            steering = -1 * steering

        trimmed_steering = steering
        if steering > 0:
            trimmed_steering = (self.steering_max - self.steering_trim) * steering + self.steering_trim
        elif steering < 0:
            trimmed_steering = (self.steering_trim - self.steering_min) * steering + self.steering_trim
        else:
            trimmed_steering = self.steering_trim

        return round(trimmed_steering, 2)

    def to_json(self):

        json_cmd = {
            'steering_trim': self.steering_trim,
            'steering_max': self.steering_max,
            'steering_min': self.steering_min,
            'steering_reversed': self.steering_reversed,
            'throttle_trim': self.throttle_trim,
            'throttle_fwd_max': self.throttle_fwd_max,
            'throttle_fwd_min': self.throttle_fwd_min,
            'throttle_rev_max': self.throttle_rev_max,
            'throttle_rev_min': self.throttle_rev_min,
        }

        return json_cmd

    def from_json(self, json_cmd):

        if 'steering_trim' in json_cmd:
            self.set_steering_trim(json_cmd['steering_trim'])
        if 'steering_max' in json_cmd:
            self.set_steering_max(json_cmd['steering_max'])
        if 'steering_min' in json_cmd:
            self.set_steering_min(json_cmd['steering_min'])
        if 'steering_reversed' in json_cmd:
            self.set_steering_reversed(json_cmd['steering_reversed'])
        if 'throttle_trim' in json_cmd:
            self.set_throttle_trim(json_cmd['throttle_trim'])
        if 'throttle_fwd_max' in json_cmd:
            self.set_throttle_fwd_max(json_cmd['throttle_fwd_max'])
        if 'throttle_fwd_min' in json_cmd:
            self.set_throttle_fwd_min(json_cmd['throttle_fwd_min'])
        if 'throttle_rev_max' in json_cmd:
            self.set_throttle_rev_max(json_cmd['throttle_rev_max'])
        if 'throttle_rev_min' in json_cmd:
            self.set_throttle_rev_min(json_cmd['throttle_rev_min'])
