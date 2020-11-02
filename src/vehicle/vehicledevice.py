from abc import ABC, abstractmethod


# Base abstract class for rtrcmd devices
class VehicleDevice(ABC):

    def __init__(self, logger) -> None:
        super().__init__()
        self.logger = logger

    @abstractmethod
    def update(self):
        pass
