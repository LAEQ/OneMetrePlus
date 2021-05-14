import tempfile
import time

from utils.camera import Camera
from utils.config import Config
from utils.filemanager import FileManager
from utils.lidar import Lidar
from utils.microphone import Microphone
from utils.tools import get_date_time_stringify


class Application:
    def __init__(self, _config: Config, _file_manager: FileManager,
                 _camera: Camera, _microphone: Microphone, _lidar: Lidar):
        self.config = _config
        self.file_manager = _file_manager
        self.camera = _camera
        self.microphone = _microphone
        self.lidar = _lidar

    def star_recording(self):
        file_video, file_sound, _, _ = self.file_manager.start_recording(self.id_cyclist, get_date_time_stringify())
        print(file_video)
        self.camera.start_recording(file_video)
        self.microphone.start_recording(file_sound)

    def stop_recording(self):
        self.camera.stop_recording()
        self.microphone.stop_recording()

    def set_up(self, message):
        if message in self.config.get_camera_widths():
            self.config.set_resolution(message)
        elif message == b'convert':
            files = self.file_manager.get_video_sound_tuples()
            print("Implement converter")
        elif message == b'export':
            print("Implement export")
        elif message == b'capture':
            distance = lidar.set_distance(self.config.unit)
            self.config.set_distance_edge(distance)


if __name__ == "__main__":
    config = Config()
    file_manager = FileManager(tempfile.gettempdir())
    camera = None
    microphone = None

    lidar = Lidar(port="/dev/ttyUSB0")

    app = Application(config, file_manager, camera, microphone, lidar)
    app.set_up(b'capture')


