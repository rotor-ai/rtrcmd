from abc import ABCMeta, abstractmethod


class VehicleSensor(metaclass=ABCMeta):
    """
    This interface class should be used for any sensor created for the vehicle. The purpose is to provide a consistent
    interface for getting data from sensors.
    """

    """
    Starts the sensor by kicking off an IO specific thread for reading from the sensor
    """
    @abstractmethod
    def start(self):
        pass

    """
    Immediately returns the most recently received sensor value
    """
    @abstractmethod
    def get_data(self) -> dict:
        pass

    """
    Stops the IO thread and performs any necessary cleanup of the sensor
    """
    @abstractmethod
    def stop(self):
        pass
