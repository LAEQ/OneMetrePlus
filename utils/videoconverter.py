import os
import glob
import subprocess

class VideoConverter:
    """Wrapper to communicate with ffmpeg library"""

    def __init__(self, files):
        self.files = files

    def convert_videos(self):
        for f in self.files:
            self.convert(f)

    def convert(self, args):
        command = "ffmpeg -framerate 25 -i {} -c copy {}".format(args[0], args[1])
        return subprocess.call(command, shell=True)


if __name__ == "__main__":
    videos = glob.glob("captures/video/*")
    videos.sort()

    exports = [file.replace("video", "export").replace("h264", "mp4") for file in videos]

    files = zip(videos, exports)

    converter = VideoConverter(files)
    converter.convert_videos()
