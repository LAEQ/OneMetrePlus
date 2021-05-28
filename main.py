"""
One meter plus (1M+): a multifunctional open source sensor for bicycles based on raspberry pi

Hardware:
    - RPi Camera (G), Fisheye Lens Angle of View (diagonal) : 160 degree,5 megapixel OV5647 sensor
    - Beitian BN-880 GPS, Level Positioning Precision: 2m At Open, Wind, Output Frequency:1Hz-10Hz,Default 1Hz
    - TFMini Plus - Micro LiDAR Module, Operating Range - 0.1m~12m, Distance resolution - 5mm, Frame rate - 1-1000Hz(adjustable)

Hardware: Andres Henao <carlosa.henaof@inrs.ca>
Software:
    - Andres Henao <carlosa.henaof@inrs.ca>
    - David Maignan <davidmaignan@gmail.com>

Supervisor:
    - Philippe Apparicio <philippe.apparicio@inrs.ca>

Source code: url to provide
Licence: GPLv3 - https://www.gnu.org/licenses/quick-guide-gplv3.html

"""
import os
from utils.camera import Camera
from utils.export import Exporter
from utils.gps import GPS
from utils.microphone import Microphone
from utils.videoconverter import VideoConverter
from utils.config import Config
from utils.filemanager import FileManager
from utils.lidar import Lidar
from utils.screen import Screen
from utils.tools import get_date, get_time, get_date_time_stringify


if __name__ == '__main__':
    start = b''
    record = True

    setting_file = os.path.join(os.path.dirname(__file__), "settings.yml")

    if os.path.exists(setting_file) is False:
        print("Setting file is not found.\n".format(setting_file))
        exit(1)

    config = Config(setting_file)

    if os.path.exists(config.capture_dir) is False:
        print("Capture directory {} is not found.\n".format(config.capture_dir))
        exit(1)

    file_manager = FileManager(config.capture_dir)
    camera = Camera()
    screen = Screen(port="/dev/ttyUSB2")
    lidar = Lidar(port="/dev/ttyUSB0", _config=config, _screen=screen)
    gps = GPS("/dev/ttyUSB1", 9600, _screen=screen)

    screen.menu()

    while True:
        page_counter = screen.read()
        screen.set_date(get_date())
        screen.set_time(get_time())

        while page_counter == b'record':
            screen.clear()
            screen.show_raspberry()

            # Reading input of screen touch nextion (waiting: start)
            while start == b'':
                start = screen.read()
                screen.set_time_recording(get_time())

                # start process of: camera, gps and distance sensor.
                if start == b'start':
                    file_video, file_distance, \
                        file_gps = file_manager.start_recording(config.id_cyclist, get_date_time_stringify())

                    camera.set_config(config)
                    camera.start_recording(file_video)
                    lidar.start_recording(file_distance)
                    gps.start_recording(file_gps)
                    screen.show_recording()

                    while record is True:
                        stop = screen.read()
                        screen.set_time_recording(get_time())

                        if stop == b'stop':
                            record = False
                            page_counter = b'record'

                        if stop == b'home':
                            record = False
                            page_counter = b''

                    camera.stop_recording()
                    lidar.stop_recording()
                    gps.stop_recording()
                    screen.clear()

                if start == b'home':  # In/out page1
                    page_counter = b''

            record = True
            start = b''

        while page_counter == b'setup':
            format_serial = screen.read()

            if format_serial == b'home':  # In/out page 2
                page_counter = b''
            elif format_serial == b'in' or format_serial == b'cm':
                config.set_unit(format_serial)

        while page_counter == b'format':
            # Settings (resolution, distance, export, convert)
            screen.set_distance(config.get_distance_edge())

            capture_serial = screen.read()
            exporter = None

            try:
                exporter = Exporter()
                screen.set_usb_plug()
            except:
                pass

            if capture_serial == b'home':
                page_counter = b''
            elif capture_serial == b'capture':
                distance = lidar.read_distance_to_edge()
                config.set_distance_edge(distance)
                screen.set_distance(config.get_distance_edge())
            elif capture_serial == b'convert':
                screen.convert_start()
                try:
                    converter = VideoConverter(file_manager.get_video_sound_tuples())
                    converter.convert_videos()
                    screen.convert_end()
                except:
                    screen.convert_error()
            elif capture_serial == b'export':
                try:
                    exporter.export(file_manager)
                    screen.export_end()
                except:
                    screen.export_error()
            elif config.is_valid_width(capture_serial):
                config.set_resolution(capture_serial)

        while page_counter == b'delete':

            delete_serial = screen.read()
            if delete_serial == b'home':
                page_counter = b''
            elif delete_serial == b'delete':
                screen.delete_start()
                try:
                    file_manager.delete_files()
                    screen.delete_end()
                    page_counter = b''
                    screen.menu()
                except:
                    pass
                finally:
                    delete_serial = b''
