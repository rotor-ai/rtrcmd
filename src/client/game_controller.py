from inputs import devices

from src.common.threadable_behavior import ThreadableBehavior


class GameController(ThreadableBehavior):

    def __init__(self, gamepad_instance):
        super().__init__()
        self._controller = gamepad_instance
        self._thread.behave = lambda: self.scan_for_events()
        self._responses = dict()

    def add_event_response(self, code, action):
        self._responses[code] = action

    def scan_for_events(self):
        event = self._controller.read()[0]
        response = self._responses.get(event.code)
        if response is not None:
            response(event.state)

