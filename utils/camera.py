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
        # self.camera = picamera.PiCamera()
        # self.camera.framerate = 24
        # self.camera.rotation = 180
        # self.camera.annotate_background = picamera.Color("black")
        # self.camera.annotate_text_size = 12
        self.config = _config
        self.ffmpeg_process = None

    def set_config(self, configuration: Config) -> None:
        pass
        # self.camera.resolution = configuration.camera_resolution()

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

    # "ffmpeg -f video4linux2 -input_format h264 -video_size 1280x720 -framerate 30 -i /dev/video0 -vcodec copy -an test.h264"


    def start_ffmpeg_recording(self, file):
        # command = self.get_record_command(file)
        # args = command.split(" ")
        #
        # command = "ffmpeg -y -f video4linux2 -input_format h264 -video_size 1280x720 -framerate 30 -i /dev/video0 -vcodec copy -an {} &".format(file)
        # command = "ffmpeg -f v4l2 -re -vsync 1 -r 2 -i /dev/video0 -f alsa -async 1 -thread_queue_size 1024 -i hw:0,0 " \
        #     "-vcodec copy -b:v 6000k -acodec aac -f segment -strftime 1 -segment_time 300 -reset_timestamps 1 " \
        #     "-segment_format mkv {}".format(file)

        command = "ffmpeg -y -thread_queue_size 1024 -use_wallclock_as_timestamps 1 -re -vsync 1 -async 1 -ar 11025 -acodec pcm_s32le -ac 1 -f alsa " \
                  "-i plughw:0 -f video4linux2 -input_format h264 -video_size 960x540 -framerate 25 -itsoffset 0.5 " \
                  " -i /dev/video0 -c:v copy -metadata:s:v:0 rotate=0 {}".format(file)

        command = "ffmpeg -y -use_wallclock_as_timestamps 1 -re -vsync 1 -async 1 -ar 11025 -acodec pcm_s32le -ac 1 -f alsa " \
                  "-thread_queue_size 1024 -i plughw:0 -f video4linux2 -input_format h264 -video_size 960x540 -framerate 25 -itsoffset 0.5 " \
                  "-thread_queue_size 1024 -i /dev/video0 -c:v copy -metadata:s:v:0 rotate=0 {}".format(file)

        command = "ffmpeg -y -use_wallclock_as_timestamps 1 -re " \
                  "-thread_queue_size 4096 -vsync 1 -ar 11025 -ac 1 -f alsa -acodec pcm_s32le -i plughw:0  " \
                  "-thread_queue_size 4096 -async 1 -f video4linux2 -input_format h264 -video_size 960x540 -framerate 25 -itsoffset 0.5 -i /dev/video0 " \
                  "-c:v copy -c:a aac -metadata:s:v:0 rotate=0 {} &".format(file)

        os.system(command)
        # self.ffmpeg_process = subprocess.Popen(args=command, stdout=subprocess.DEVNULL, shell=True)

    def stop_ffmpeg_recording(self):
        print(self.ffmpeg_process)
        os.system("pkill ffmpeg")
        # self.ffmpeg_process.terminate()


if __name__ == "__main__":
    config = Config()
    camera = Camera(config)
    file = "test.h264"
    camera.start_ffmpeg_recording(file)
    time.sleep(25)
    camera.stop_ffmpeg_recording()
    print("Test")
    # print(process)
    # time.sleep(20)
    # process.terminate()



