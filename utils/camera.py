import time
import os

from utils.config import Config
from utils.tools import get_date_time
import subprocess


class Camera:
    def __init__(self):
        self.framerate = 25
        self.rotation = 180
        self.recording_process = None

    def set_config(self, configuration: Config) -> None:
        self.width, self.height = configuration.camera_resolution()

    def get_record_command(self, file):        
        return "raspivid -t 5000000 -rot {} -fps {} -w {} -h {} -ae 15,0xff,0x808000 -a 1024 -a 12 -o {}".format(
            self.rotation, self.framerate, self.width, self.height,file
        )

    def start_recording(self, file):
        if self.recording_process is not None and self.recording_process.poll() is not None:
            self.recording_process.terminate()

        command = self.get_record_command(file)
        args = command.split(" ")
        print (args)
        self.recording_process = subprocess.Popen(args=args,
                                                  stdout=subprocess.DEVNULL,
                                                  stderr=subprocess.STDOUT,
                                                  close_fds=True)

    def stop_recording(self):
        self.recording_process.terminate()


if __name__ == "__main__":
    config = Config()
    camera = Camera()
    camera.set_config(config)

    file = "testvideo.h264"
    camera.start_recording(file)
    time.sleep(5)
    camera.stop_recording()




