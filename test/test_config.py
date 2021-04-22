import os
import unittest
import tempfile
import re

from datetime import datetime as dt
from pathlib import Path
from config import Config


def create_files(total, config, timestamp):
    for i in range(total):
        prefix = "prefix_{}".format(i)
        video_file, sound_file, \
        distance_file, gps_file = config.start(prefix, timestamp)

        Path(video_file).touch()
        Path(sound_file).touch()
        Path(distance_file).touch()
        Path(gps_file).touch()


class TestConfig(unittest.TestCase):
    """
    Testing configuration with real file system
    @todo: mock file system
    """
    def setUp(self) -> None:
        self.home = tempfile.mkdtemp()

    def test_init(self):
        config = Config(home=self.home)
        result = True
        for directory in config.dir_paths:
            result = result and os.path.exists(directory)

        self.assertTrue(result)

    def test_start(self):
        config = Config(home=self.home)
        timestamp = "2021_04_21_13_55_56"
        prefix = "prefix"
        video_file, sound_file, \
        distance_file, gps_file = config.start(prefix, timestamp)

        self.assertEqual(
            video_file,
            os.path.join(self.home, "video", "{}_{}.h264".format(prefix, timestamp))
        )

        self.assertEqual(
            sound_file,
            os.path.join(self.home, "sound", "{}_{}.wav".format(prefix, timestamp))
        )

        self.assertEqual(
            distance_file,
            os.path.join(self.home, "distance", "{}_{}.csv".format(prefix, timestamp))
        )

        self.assertEqual(
            gps_file,
            os.path.join(self.home, "gps", "{}_{}.csv".format(prefix, timestamp))
        )

    def test_get_videos(self):
        pattern = re.compile('.+h264$')
        config = Config(home=self.home)
        timestamp = "timestamp"

        create_files(3, config, timestamp)
        video_files = config.get_videos()

        self.assertEqual(3, len(video_files))
        self.assertTrue(bool(pattern.match(video_files[0])))
        self.assertTrue(bool(pattern.match(video_files[1])))
        self.assertTrue(bool(pattern.match(video_files[2])))

    def test_get_sounds(self):
        pattern = re.compile('.+wav$')
        config = Config(home=self.home)
        timestamp = "timestamp"

        create_files(2, config, timestamp)
        files = config.get_sounds()

        self.assertEqual(2, len(files))
        self.assertTrue(bool(pattern.match(files[0])))
        self.assertTrue(bool(pattern.match(files[1])))

    def test_get_gps(self):
        pattern = re.compile('.+csv$')
        config = Config(home=self.home)
        timestamp = "timestamp"

        create_files(4, config, timestamp)
        files = config.get_gps()

        self.assertEqual(4, len(files))
        self.assertTrue(bool(pattern.match(files[0])))
        self.assertTrue(bool(pattern.match(files[1])))
        self.assertTrue(bool(pattern.match(files[2])))
        self.assertTrue(bool(pattern.match(files[3])))

    def test_get_distance(self):
        pattern = re.compile('.+csv$')
        config = Config(home=self.home)
        timestamp = "timestamp"

        create_files(8, config, timestamp)
        files = config.get_distance()

        self.assertEqual(8, len(files))
        self.assertTrue(bool(pattern.match(files[0])))
        self.assertTrue(bool(pattern.match(files[1])))
        self.assertTrue(bool(pattern.match(files[2])))
        self.assertTrue(bool(pattern.match(files[3])))
        self.assertTrue(bool(pattern.match(files[4])))
        self.assertTrue(bool(pattern.match(files[5])))
        self.assertTrue(bool(pattern.match(files[6])))
        self.assertTrue(bool(pattern.match(files[7])))

    def test_get_all_files(self):
        config = Config(home=self.home)
        timestamp = "timestamp"

        create_files(64, config, timestamp)
        files = config.get_all_files()
        self.assertEqual(64 * 4, len(files))

        # @todo assert (8 videos, 8 sounds, ...)

    def test_get_export(self):
        config = Config(home=self.home)
        timestamp = dt.now().isoformat()
        create_files(6, config, timestamp)

        exports = config.get_video_sound_tuples()
        self.assertEqual(6, len(tuple(exports)))