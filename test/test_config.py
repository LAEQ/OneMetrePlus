import unittest
import os

from utils.config import Config


class TestConfig(unittest.TestCase):
    def setUp(self) -> None:
        file = os.path.join(os.path.dirname(__file__), "settings.yml")
        self.config = Config(file)

    def test_settings(self):
        self.assertEqual(300, self.config.gps_period_capture)
        self.assertEqual(1, self.config.unit)
        self.assertEqual(100, self.config.warning_distance)
        self.assertEqual(300, self.config.max_distance)
        self.assertEqual(0, self.config.distance_edge)
        self.assertEqual(25, self.config.frame_rate)
        self.assertEqual((800, 600), self.config.get_resolution())
        self.assertIsNotNone(self.config.project_home)
        self.assertIsNotNone(self.config.capture_dir)

    def test_default_resolution(self):
        self.assertEqual((800, 600), self.config.get_resolution())

    def test_set_resolution_800(self):
        self.config.set_resolution(b'800')
        self.assertEqual((800, 600), self.config.get_resolution())

    def test_set_resolution_600(self):
        self.config.set_resolution(b'600')
        self.assertEqual((600, 450), self.config.get_resolution())

    def test_set_resolution_400(self):
        self.config.set_resolution(b'400')
        self.assertEqual((400, 300), self.config.get_resolution())

    def test_get_camera_widths(self):
        self.config.get_camera_widths()
        self.assertListEqual([b'400', b'600', b'800'], self.config.get_camera_widths())

    def test_is_valid_width(self):
        values = [b"400", b"600", b"800"]
        for value in values:
            with self.subTest(i=value):
                self.assertTrue(self.config.is_valid_width(value))

    def test_set_unit_inch(self):
        self.config.set_unit(b'in')
        self.assertEqual(0.393701, self.config.unit)

    def test_set_unit_cm(self):
        self.config.set_unit(b'cm')
        self.assertEqual(1, self.config.unit)


if __name__ == "__main__":
    suite = unittest.makeSuite(TestConfig)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
