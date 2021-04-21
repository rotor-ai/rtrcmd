import logging
import threading

class GameControllerCalibration():

    def __init__(self):
        self.left_trigger_max = 0
        self.right_trigger_max = 0
        self.joystick_boundary = 0

    def to_json(self):
        return self.__dict__

    def from_json(self, input_json):
        if input_json.__contains__('left_trigger_max'):
            self.left_trigger_max = input_json['left_trigger_max']
        if input_json.__contains__('right_trigger_max'):
            self.right_trigger_max = input_json['right_trigger_max']
        if input_json.__contains__('joystick_boundary'):
            self.joystick_boundary = input_json['joystick_boundary']


class GameController:

    def __init__(self, game_controller_instance, calibration=GameControllerCalibration()):
        super().__init__()
        self._calibration = calibration
        self._controller = game_controller_instance
        self._thread = GameControllerThread()
        self._thread.set_behavior(lambda: self.scan_for_events())
        self._responses = dict()

    def start(self):
        self._thread.start()

    def stop(self):
        self._thread.set_behavior(lambda: False)

    def add_event_response(self, code, action):
        self._responses[code] = action

    def get_calibration(self):
        return self._calibration

    def scan_for_events(self):
        event = self._controller.read()[0]
        response = self._responses.get(event.code)
        if response is not None:
            response(event.state)

        return True


class GameControllerThread(threading.Thread):

    def __init__(self):
        super().__init__()
        self._should_continue = True

    def set_behavior(self, behavior):
        self.behave = behavior

    def run(self) -> None:
        super().run()

        while self._should_continue:
            self._should_continue = self.behave()

        logging.info("ENDING " + str(self.__class__) + "THREAD")
