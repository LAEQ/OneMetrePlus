import os
import unittest
import tempfile
import re

from datetime import datetime as dt
from pathlib import Path

from utils.filemanager import FileManager


def create_files(total, manager, timestamp):
    for i in range(total):
        prefix = "prefix_{}".format(i)
        video_file, sound_file, \
            distance_file, gps_file = manager.start_recording(prefix, timestamp)

        Path(video_file).touch()
        Path(sound_file).touch()
        Path(distance_file).touch()
        Path(gps_file).touch()


class TestFileManager(unittest.TestCase):
    """
    Dependency with file system
    """

    def setUp(self) -> None:
        self.home = tempfile.mkdtemp()

    def test_init(self):
        manager = FileManager(home=self.home)
        result = True
        for directory in manager.dir_paths:
            result = result and os.path.exists(directory)

        self.assertTrue(result)

    def test_start(self):
        manager = FileManager(home=self.home)
        timestamp = "2021_04_21_13_55_56"
        prefix = "prefix"
        video_file, sound_file, \
            distance_file, gps_file = manager.start(prefix, timestamp)

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
        manager = FileManager(home=self.home)
        timestamp = "timestamp"

        create_files(3, manager, timestamp)
        video_files = manager.get_videos()

        self.assertEqual(3, len(video_files))
        self.assertTrue(bool(pattern.match(video_files[0])))
        self.assertTrue(bool(pattern.match(video_files[1])))
        self.assertTrue(bool(pattern.match(video_files[2])))

    def test_get_sounds(self):
        pattern = re.compile('.+wav$')
        manager = FileManager(home=self.home)
        timestamp = "timestamp"

        create_files(2, manager, timestamp)
        files = manager.get_sounds()

        self.assertEqual(2, len(files))
        self.assertTrue(bool(pattern.match(files[0])))
        self.assertTrue(bool(pattern.match(files[1])))

    def test_get_gps(self):
        pattern = re.compile('.+csv$')
        manager = FileManager(home=self.home)
        timestamp = "timestamp"

        create_files(4, manager, timestamp)
        files = manager.get_gps()

        self.assertEqual(4, len(files))
        self.assertTrue(bool(pattern.match(files[0])))
        self.assertTrue(bool(pattern.match(files[1])))
        self.assertTrue(bool(pattern.match(files[2])))
        self.assertTrue(bool(pattern.match(files[3])))

    def test_get_distance(self):
        pattern = re.compile('.+csv$')
        manager = FileManager(home=self.home)
        timestamp = "timestamp"

        create_files(8, manager, timestamp)
        files = manager.get_distance()

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
        manager = FileManager(home=self.home)
        timestamp = "timestamp"

        create_files(64, manager, timestamp)
        files = manager.get_all_files()
        self.assertEqual(64 * 4, len(files))

        # @todo assert (8 videos, 8 sounds, ...)

    def test_get_export(self):
        manager = FileManager(home=self.home)
        timestamp = dt.now().isoformat()
        create_files(6, manager, timestamp)

        exports = manager.get_video_sound_tuples()
        self.assertEqual(6, len(tuple(exports)))
        
    def test_delete_files(self):
        manager = FileManager(home=self.home)
        timestamp = dt.now().isoformat()
        create_files(6, manager, timestamp)

        manager.delete_files()
        self.assertEqual(0, len(manager.get_all_files()))


if __name__ == "__main__":
    suite = unittest.makeSuite(TestFileManager)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
