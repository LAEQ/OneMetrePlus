import unittest

from utils.tools import unit_system, get_time, get_date, get_date_time_stringify, get_date_time


class TestUnit(unittest.TestCase):
    def test_unit_imperial(self):
        self.assertEqual(0.393701, unit_system(b'in'))

    def test_unit_meter(self):
        self.assertEqual(1, unit_system(b'cm'))

    def test_unit_default(self):
        self.assertEqual(1, unit_system(b'mock'))


class TestDateTime(unittest.TestCase):
    def test_get_time(self):
        self.assertRegex(get_time(), "[0-9]{2}:[0-9]{2}:[0-9]{2}")

    def test_get_date(self):
        self.assertRegex(get_date(), "[0-9]{4}-[0-9]{2}-[0-9]{2}")

    def test_get_timestamp(self):
        self.assertRegex(get_date_time_stringify(), "[0-9]{4}_[0-9]{2}_[0-9]{2}_[0-9]{2}_[0-9]{2}_[0-9]{2}")

    def test_get_date_time(self):
        self.assertRegex(get_date_time(), "[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}")


if __name__ == "__main__":
    suite = unittest.makeSuite(TestUnit)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

    suite = unittest.makeSuite(TestDateTime)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
