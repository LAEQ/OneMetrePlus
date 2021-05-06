import os


class VideoConverter:
    """Wrapper to communicate with ffmpeg library"""

    def __init__(self):
        pass

    def convert_videos(self, files):
        for f in files:
            print(f)

    def convert(self, video_file, sound_file, dest_file):
        command = "ffmpeg -i {} -i {} -c:v copy -c:a aac -shortest {}".format(video_file, sound_file, dest_file)
        os.system(command)
