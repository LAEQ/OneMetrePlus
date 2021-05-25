import os
import subprocess
import time

import ffmpeg
import picamera
import cv2

from utils.config import Config
from utils.tools import get_date_time


class Camera:
    def __init__(self, _config: Config):
        self.camera = picamera.PiCamera()
        self.camera.framerate = _config.frame_rate
        self.camera.rotation = 0
        self.camera.annotate_background = picamera.Color("black")
        self.camera.annotate_text_size = 12
        self.config = _config
        self.ffmpeg_process = None
        self.camera.resolution = self.config.get_resolution()

    def set_config(self, configuration: Config) -> None:
        self.camera.resolution = configuration.get_resolution()

    def start_recording(self, file_path: str) -> None:
        self.camera.annotate_text = get_date_time()
        self.camera.start_recording(file_path)

    def stop_recording(self) -> None:
        self.camera.stop_recording()

    def get_record_command(self, file):
        width, height = self.config.get_resolution()
        resolution = "{}x{}".format(width, height)
        return "ffmpeg -f video4linux2 -input_format h264 -video_size {} " \
               "-framerate 30 -i /dev/video0 -vcodec copy -an {}".format(resolution, file)

    def start_ffmpeg_recording(self, _file):
        command = "ffmpeg -y -use_wallclock_as_timestamps 1 -re " \
                  "-thread_queue_size 4096 -vsync 1 -ar 25000 -ac 1 -f alsa -acodec pcm_s32le -i plughw:0  " \
                  "-thread_queue_size 4096 -async 1 -f video4linux2 -input_format h264 -video_size 960x540 " \
                  "-framerate 25 -i /dev/video0 " \
                  "-c:v copy -c:a aac -metadata:s:v:0 rotate=0 {}".format(_file)

        self.ffmpeg_process = subprocess.Popen(args=command, shell=True)

    def stop_ffmpeg_recording(self):
        self.ffmpeg_process.terminate()


if __name__ == "__main__":
    config = Config()
    camera = Camera(_config=config)
    file = "/home/pi/captures/video/camera_stream.mp4"
    camera.start_ffmpeg_recording(file)
    time.sleep(10)
    camera.stop_ffmpeg_recording()
    print("Test")




