import time

from utils.camera import Camera
from utils.config import Config
from utils.microphone import Microphone

if __name__ == "__main__":
    camera = Camera()
    microphone = Microphone()
    config = Config()

    video_file = "test.h264"
    sound_file = "test.wav"

    camera.set_config(config)

    print("Start recording")
    camera.start_recording(video_file)
    microphone.start_recording(sound_file)

    time.sleep(60)

    camera.stop_recording()
    microphone.stop_recording()

    print("Stop Recording")
