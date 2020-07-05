from abc import ABC, abstractmethod


# Base abstract class for rtrcmd devices
class VehicleDevice(ABC):

    @abstractmethod
    def update(self):
        pass
