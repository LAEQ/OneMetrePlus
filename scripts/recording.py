from __future__ import print_function, division

import time


from utils.camera import Camera
from utils.config import Config
from utils.microphone import Microphone

if __name__ == "__main__":
    print("Start recording")
    microphone = Microphone(_rate=25000)
    camera = Camera(_config=Config())

    microphone.start_recording("/home/pi/captures/sound/video.wav")
    camera.start_recording("/home/pi/captures/video/video.h264")
    time.sleep(300)

    microphone.stop_recording()
    camera.stop_recording()

    print("Stop Recording")


