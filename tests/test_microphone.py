import unittest

from utils.microphone import Microphone


class TestMicrophone(unittest.TestCase):
    def setUp(self) -> None:
        self.microphone = Microphone()

    def test_get_record_command(self):
        self.assertTrue(True)


if __name__ == "__main__":
    suite = unittest.makeSuite(TestMicrophone)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
