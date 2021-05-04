import os
import glob


class FileManager:
    """
    Manager  for capturing, exporting and deleting video, sound, gps and distance files
    """
    def __init__(self, home="~/Desktop/Capture/files"):
        self.home = home
        self.directories = ["sound", "video", "gps", "distance", "export"]
        self.dir_paths = [os.path.join(self.home, folder) for folder in self.directories]

        # Create app structure
        self.init()

    def init(self):
        for f in self.dir_paths:
            if os.path.exists(f) is False:
                os.makedirs(f)

    def sound_path(self):
        return self.dir_paths[0]

    def video_path(self):
        return self.dir_paths[1]

    def gps_path(self):
        return self.dir_paths[2]

    def distance_path(self):
        return self.dir_paths[3]

    def export_path(self):
        return self.dir_paths[4]

    def new_gps(self, prefix, timestamp):
        return os.path.join(self.gps_path(), "{}_{}.csv".format(prefix, timestamp))

    def new_distance(self, prefix, timestamp):
        return os.path.join(self.distance_path(), "{}_{}.csv".format(prefix, timestamp))

    def new_video(self, prefix, timestamp):
        return os.path.join(self.video_path(), "{}_{}.h264".format(prefix, timestamp))

    def new_sound(self, prefix, timestamp):
        return os.path.join(self.sound_path(), "{}_{}.wav".format(prefix, timestamp))

    def start(self, prefix, timestamp):
        return self.new_video(prefix, timestamp), \
               self.new_sound(prefix, timestamp), \
               self.new_distance(prefix, timestamp), \
               self.new_gps(prefix, timestamp)

    def get_videos(self):
        return glob.glob(os.path.join(self.video_path(), "*"))

    def get_sounds(self):
        return glob.glob(os.path.join(self.sound_path(), "*"))

    def get_gps(self):
        return glob.glob(os.path.join(self.gps_path(), "*"))

    def get_distance(self):
        return glob.glob(os.path.join(self.distance_path(), "*"))

    def get_video_sound_tuples(self):
        video_files = self.get_videos()
        sound_files = self.get_sounds()

        video_files.sort()
        sound_files.sort()

        return zip(video_files, sound_files)

    def get_all_files(self):
        return self.get_videos() + self.get_sounds() + self.get_gps() + self.get_distance()
