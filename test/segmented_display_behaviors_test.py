import unittest
from unittest.mock import Mock

from src.vehicle.segmented_display_behaviors import address_display

class SegmentedDisplayTest(unittest.TestCase):

    def test_should_display_ip_address(self):

        fake_network_interface = [[], [], [dict({'addr': '192.168.1.2'})]]
        mock_display = Mock()
        mock_display.run_duration = Mock(return_value=0)
        mock_display.loop_delay = Mock(return_value=0.5)
        mock_display.set_text = Mock()

        address_display(mock_display, fake_network_interface)

        mock_display.set_text.assert_called_once_with("    192.168.1.2")
