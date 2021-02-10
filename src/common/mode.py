from enum import IntEnum


class ModeType(IntEnum):
    NORMAL = 0
    TRAIN = 1
    AUTO = 2
    ASSISTED = 3


class Mode(object):

    def __init__(self):
        self._mode_type = ModeType.NORMAL

    def set_mode(self, mode_type):

        # Check if the mode type is actually a valid member of the Enum
        values = set(item.value for item in ModeType)
        if mode_type not in values:
            raise Exception("Invalid mode type")

        self._mode_type = mode_type

    def get_mode(self):
        return self._mode_type

    def get_mode_name(self):
        if self._mode_type == ModeType.NORMAL:
            return "NORMAL"
        elif self._mode_type == ModeType.TRAIN:
            return "TRAIN"
        elif self._mode_type == ModeType.AUTO:
            return "AUTO"
        elif self._mode_type == ModeType.ASSISTED:
            return "ASSISTED"

    def to_json(self):

        json_mode = {
            'mode': int(self._mode_type)
        }

        return json_mode

    def from_json(self, json_mode):

        if 'mode' not in json_mode:
            raise Exception("Cannot parse mode from json")

        self.set_mode(json_mode['mode'])
