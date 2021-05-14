import unittest

from utils.config import Config


class TestConfig(unittest.TestCase):
    def setUp(self) -> None:
        self.config = Config()

    def test_get_camera_widths(self):
        result = self.config.get_camera_widths()

        self.assertListEqual([b"800", b"600", b"400"], result)

    def test_default_resolution(self):
        self.assertEqual((400, 300), self.config.get_resolution())

    def test_set_resolution_800(self):
        result = self.config.set_resolution(b'800')
        self.assertEqual((800, 600), result)

    def test_set_resolution_600(self):
        result = self.config.set_resolution(b'600')
        self.assertEqual((600, 450), result)

    def test_set_resolution_400(self):
        result = self.config.set_resolution(b'400')
        self.assertEqual((400, 300), result)

    def test_set_resolution_no_match(self):
        result = self.config.set_resolution(b'100')
        self.assertEqual((400, 300), result)

    def test_is_valid_width(self):
        values = [b"400", b"600", b"800"]
        for value in values:
            with self.subTest(i=value):
                self.assertTrue(self.config.is_valid_width(value))

    def test_get_max_distance_cm(self):
        result = self.config.get_max_distance()
        self.assertEqual(300, result)

    def test_get_max_distance_in(self):
        self.config.set_unit(b'in')
        result = self.config.get_max_distance()
        self.assertAlmostEqual(118.1103000000000, result)


if __name__ == "__main__":
    suite = unittest.makeSuite(TestConfig)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
