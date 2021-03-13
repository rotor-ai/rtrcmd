import unittest
from unittest.mock import Mock

from ..src.vehicle.segmented_display_behaviors import address_display


class SegmentedDisplayTest(unittest.TestCase):

    def test_should_display_ip_address(self):

        fake_network_interface = [[], [], [dict({'addr': '192.168.1.2'})]]
        mock_display = Mock()
        mock_display.run_duration = Mock(return_value=0)
        mock_display.loop_delay = Mock(return_value=0.5)
        mock_display.set_text = Mock()

        address_display(mock_display, fake_network_interface)

        mock_display.set_text.assert_called_once_with("    ")

    def test_should_display_offset_ip_address_with_offset(self):
        fake_network_interface = [[], [], [dict({'addr': '192.168.1.2'})]]
        mock_display = Mock()
        mock_display.run_duration = Mock(return_value=3.5)
        mock_display.loop_delay = Mock(return_value=0.5)
        mock_display.set_text = Mock()

        address_display(mock_display, fake_network_interface)

        mock_display.set_text.assert_called_once_with("168.1.")

    def test_should_wrap_around(self):
        fake_network_interface = [[], [], [dict({'addr': '192.168.1.2'})]]
        mock_display = Mock()
        mock_display.run_duration = Mock(return_value=8)
        mock_display.loop_delay = Mock(return_value=0.5)
        mock_display.set_text = Mock()

        address_display(mock_display, fake_network_interface)

        mock_display.set_text.assert_called_once_with("192.1")

    def test_should_wrap_around_boundry(self):
        fake_network_interface = [[], [], [dict({'addr': '192.168.1.2'})]]
        mock_display = Mock()
        mock_display.run_duration = Mock(return_value=5)
        mock_display.loop_delay = Mock(return_value=0.5)
        mock_display.set_text = Mock()

        address_display(mock_display, fake_network_interface)

        mock_display.set_text.assert_called_once_with("1.2  ")

    def test_should_handle_situation_when_key_not_present(self):

        fake_network_interface = [[], [], [dict()]]
        mock_display = Mock()
        mock_display.run_duration = Mock(return_value=2)
        mock_display.loop_delay = Mock(return_value=0.5)
        mock_display.set_text = Mock()

        address_display(mock_display, fake_network_interface)

        mock_display.set_text.assert_called_once_with("127.0.")

    def test_should_handle_situation_when_network_object_does_not_contain_second_index_zero(self):
        fake_network_interface = [[], [], []]
        mock_display = Mock()
        mock_display.run_duration = Mock(return_value=2)
        mock_display.loop_delay = Mock(return_value=0.5)
        mock_display.set_text = Mock()

        address_display(mock_display, fake_network_interface)

        mock_display.set_text.assert_called_once_with("127.0.")

    def test_should_handle_situation_when_network_object_does_not_contain_first_index_two(self):
        fake_network_interface = [[], []]
        mock_display = Mock()
        mock_display.run_duration = Mock(return_value=2)
        mock_display.loop_delay = Mock(return_value=0.5)
        mock_display.set_text = Mock()

        address_display(mock_display, fake_network_interface)

        mock_display.set_text.assert_called_once_with("127.0.")
