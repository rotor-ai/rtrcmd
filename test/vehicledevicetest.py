import unittest

from vehicledevice import VehicleDevice


class VehicleLightTest(unittest.TestCase):

    def test_should_require_abstract_method_update(self):
        class SomeVehicleDevice(VehicleDevice):
            pass

        self.assertRaises(TypeError, lambda: SomeVehicleDevice())
