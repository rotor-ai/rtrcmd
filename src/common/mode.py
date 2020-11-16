from enum import IntEnum


class ModeType(IntEnum):
    NORMAL = 0
    TRAIN = 1
    AUTO = 2


class Mode(object):

    def __init__(self):
        self.mode_type = ModeType.NORMAL

    def set_mode(self, mode_type):

        # Check if the mode type is actually a valid member of the Enum
        values = set(item.value for item in ModeType)
        if mode_type not in values:
            raise Exception("Invalid mode type")

        self.mode_type = mode_type

    def get_mode(self):
        return self.mode_type

    def to_json(self):

        json_mode = {
            'mode': int(self.mode_type)
        }

        return json_mode

    def from_json(self, json_cmd):

        if 'mode' not in json_cmd:
            raise Exception("Cannot parse mode from json")

        self.set_mode(json_cmd['mode'])
