from enum import IntEnum


class LabelIndex(IntEnum):
    LEFT = 0
    RIGHT = 1
    NEUTRAL = 2


names = ["LEFT", "RIGHT", "NEUTRAL"]
values = [-1.0, 1.0, 0]


class Label(object):

    @staticmethod
    def steering_value_to_label_index(val):
        if val < 0:
            return LabelIndex.LEFT
        elif val > 0:
            return LabelIndex.RIGHT
        elif val == 0:
            return LabelIndex.NEUTRAL

    @staticmethod
    def label_index_to_name(label_index):
        return names[label_index]

    @staticmethod
    def label_index_to_steering_value(label_index):
        return values[label_index]
