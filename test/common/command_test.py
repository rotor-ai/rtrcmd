import unittest

from src.common.command import Command
from ..context import src


class CommandTest(unittest.TestCase):

    def test_should_init_with_default_values(self):
        subject = Command()

        self.assertEqual(0.0, subject.steering)
        self.assertEqual(0.0, subject.throttle)

    def test_should_init_with_supplied_values(self):
        subject = Command(0.1, 0.2)

        self.assertEqual(0.1, subject.steering)
        self.assertEqual(0.2, subject.throttle)

    def test_getters_work(self):
        subject = Command(0.1, 0.2)

        self.assertEqual(0.1, subject.get_steering())
        self.assertEqual(0.2, subject.get_throttle())

        subject.steering = 0.3
        subject.throttle = 0.4

        self.assertEqual(0.3, subject.get_steering())
        self.assertEqual(0.4, subject.get_throttle())

    def test_setters_work(self):
        subject = Command(0.1, 0.2)
        subject.set_steering(0.3)
        subject.set_throttle(0.4)

        self.assertEqual(0.3, subject.steering)
        self.assertEqual(0.4, subject.throttle)

        subject.set_steering(0.5)
        subject.set_throttle(0.6)
        self.assertEqual(0.5, subject.steering)
        self.assertEqual(0.6, subject.throttle)

    def test_should_enforce_upper_boundary_on_steering(self):
        subject = Command()

        # test just above the upper bound to make sure it does throw an exception
        self.assertRaises(Exception, lambda: subject.set_steering(1.1))

        # test the upper bound to make sure it does not throw an exception
        subject.set_steering(1.0)

    def test_should_enforce_lower_boundary_on_steering(self):
        subject = Command()

        # test just above the upper bound to make sure it does throw an exception
        self.assertRaises(Exception, lambda: subject.set_steering(-1.1))

        # test the upper bound to make sure it does not throw an exception
        subject.set_steering(-1.0)

    def test_should_enforce_upper_boundary_on_throttle(self):
        subject = Command()

        # test just above the upper bound to make sure it does throw an exception
        self.assertRaises(Exception, lambda: subject.set_throttle(1.1))

        # test the upper bound to make sure it does not throw an exception
        subject.set_throttle(1.0)

    def test_should_enforce_lower_boundary_on_throttle(self):
        subject = Command()

        # test just above the upper bound to make sure it does throw an exception
        self.assertRaises(Exception, lambda: subject.set_throttle(-1.1))

        # test the upper bound to make sure it does not throw an exception
        subject.set_throttle(-1.0)

    def test_should_check_steering_bounds_on_init(self):

        self.assertRaises(Exception, lambda: Command(s=1.1))

    def test_should_check_throttle_bounds_on_init(self):

        self.assertRaises(Exception, lambda: Command(t=-1.1))
