import time
import picamera

from utils.config import Config
from utils.tools import get_date_time


class Camera:
    def __init__(self):
        self.camera = picamera.PiCamera()
        self.camera.framerate = 24
        self.camera.rotation = 180
        self.camera.annotate_background = picamera.Color("black")
        self.camera.annotate_text_size = 12

    def set_config(self, configuration: Config) -> None:
        self.camera.resolution = configuration.camera_resolution()

    def start_recording(self, file_path: str) -> None:
        self.camera.annotate_text = get_date_time()
        self.camera.start_recording(file_path)

    def stop_recording(self) -> None:
        self.camera.stop_recording()


if __name__ == "__main__":
    config = Config()
    camera = Camera()
    camera.set_config(config)

    file = "test.h264"
    camera.start_recording(file)
    time.sleep(5)
    camera.stop_recording()


# def get_camera(file_video, camera_resolution_width, camera_resolution_height):
#     with picamera.PiCamera() as camera:
#         camera.resolution = (camera_resolution_width, camera_resolution_height)
#         camera.framerate = 25
#         # camera.start_preview(fullscreen=False,window=(100,200,300,300))
#         camera.rotation = 180
#         camera.annotate_background = picamera.Color('black')
#         camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         camera.annotate_text_size = 12
#         camera.start_recording(file_video)
#         # camera.video_stabilization
#         start = dt.datetime.now()
#         while (dt.datetime.now() - start).seconds < 5000:  # time of recording in seconds
#             camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             camera.wait_recording(0.2)
#         camera.stop_recording()