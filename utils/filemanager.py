import os
import glob


class FileManager:
    """
    Manager  for capturing, exporting and deleting video, sound, gps and distance files
    """
    def __init__(self, home):
        self.home = home
        self.directories = ["video", "gps", "distance", "export", "switch"]
        self.dir_paths = [os.path.join(self.home, folder) for folder in self.directories]

        # Create capture structure
        self.init()

    def init(self):
        for f in self.dir_paths:
            if os.path.exists(f) is False:
                os.makedirs(f)

    def video_path(self):
        return self.dir_paths[0]

    def gps_path(self):
        return self.dir_paths[1]

    def distance_path(self):
        return self.dir_paths[2]

    def export_path(self):
        return self.dir_paths[3]

    def switch_path(self):
        return self.dir_paths[4]

    def new_gps(self, prefix, timestamp):
        return os.path.join(self.gps_path(), "{}_{}.csv".format(prefix, timestamp))

    def new_distance(self, prefix, timestamp):
        return os.path.join(self.distance_path(), "{}_{}.csv".format(prefix, timestamp))

    def new_video(self, prefix, timestamp):
        return os.path.join(self.video_path(), "{}_{}.h264".format(prefix, timestamp))
    
    def new_switch(self, prefix, timestamp):
        return os.path.join(self.switch_path(), "{}_{}.csv".format(prefix, timestamp))

    def start_recording(self, prefix, timestamp):
        return self.new_video(prefix, timestamp), \
               self.new_distance(prefix, timestamp), \
               self.new_gps(prefix, timestamp), \
               self.new_switch(prefix, timestamp)

    def get_videos(self):
        return glob.glob(os.path.join(self.video_path(), "*"))

    def get_gps(self):
        return glob.glob(os.path.join(self.gps_path(), "*"))

    def get_distance(self):
        return glob.glob(os.path.join(self.distance_path(), "*"))

    def get_export(self):
        return glob.glob(os.path.join(self.export_path(), "*"))
    
    def get_switch(self):
        return glob.glob(os.path.join(self.switch_path(), "*"))

    def get_video_sound_tuples(self):
        video_files = self.get_videos()
        export_files = [file.replace("video", "export").replace("h264", 'mp4') for file in video_files]

        video_files.sort()
        export_files.sort()

        return zip(video_files, export_files)

    def get_all_files(self):
        return self.get_videos() + self.get_gps() + self.get_distance() + self.get_export() + self.get_switch()

    def delete_files(self):
        for f in self.get_all_files():
            try:
                os.remove(f)
            except Exception as error:
                print(error)

    def delete_export_files(self):
        for f in self.get_export():
            try:
                os.remove(f)
            except Exception as error:
                print(error)

