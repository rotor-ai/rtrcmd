from abc import ABCMeta, abstractmethod


class VehicleSensor(metaclass=ABCMeta):
    """
    This interface class should be used for any sensor created for the vehicle. The purpose is to provide a consistent
    interface for getting data from sensors. When the get_data() method is called, it should return a dictionary of
    values relevant to the sensor. The function should return immediately, so a separate sensor service thread is
    recommended to perform all sensor IO/collection.
    """

    @abstractmethod
    def get_data(self) -> dict:
        pass
