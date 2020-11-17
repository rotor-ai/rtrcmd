from abc import ABCMeta, abstractmethod


class VehicleSensor(metaclass=ABCMeta):

    @abstractmethod
    def get_data(self) -> dict:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass
