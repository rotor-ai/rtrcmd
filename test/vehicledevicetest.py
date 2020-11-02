import unittest

from vehicle.vehicledevice import VehicleDevice


class VehicleDeviceTest(unittest.TestCase):

    def test_should_require_abstract_method_update(self):
        class SomeVehicleDevice(VehicleDevice):
            pass

        self.assertRaises(TypeError, lambda: SomeVehicleDevice())
