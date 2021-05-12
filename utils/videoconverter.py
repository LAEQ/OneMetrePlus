import os
import glob


class VideoConverter:
    """Wrapper to communicate with ffmpeg library"""

    def __init__(self, files):
        self.files = files

    def convert_videos(self):
        for f in self.files:
            print(f[0])
            self.convert(f)

    def convert(self, args):
        command = "ffmpeg -i {} -i {} -c:v copy -c:a aac -shortest {}".format(args[0], args[1], args[2])
        os.system(command)


if __name__ == "__main__":
    videos = glob.glob("captures/video/*")
    sounds = glob.glob("captures/sound/*")

    videos.sort()
    sounds.sort()
    exports = [file.replace("video", "export").replace("h264", "mp4") for file in videos]

    files = zip(videos, sounds, exports)

    converter = VideoConverter(files)
    converter.convert_videos()
