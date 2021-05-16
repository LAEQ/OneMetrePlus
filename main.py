"""
Raspberry project to record traffic with vehicles passing by during a bike ride.

Hardware:
    - RPi Camera (G), Fisheye Lens Angle of View (diagonal) : 160 degree,5 megapixel OV5647 sensor
    - I2S Output Digital Microphone, High SNR of 65dB(A)
    - Beitian BN-880 GPS, Level Positioning Precision: 2m At Open, Wind, Output Frequency:1Hz-10Hz,Default 1Hz
    - TFMini Plus - Micro LiDAR Module, Operating Range - 0.1m~12m, Distance resolution - 5mm, Frame rate - 1-1000Hz(adjustable)

Hardware: Andres Henao <email@toprovide>
Software:
    - Andres Henao <email@toprovide>
    - David Maignan <davidmaignan@gmail.com>

Supervisor:
    - Philippe Apparicio <philippe.apparicio@ucs.inrs.ca>

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
    initial_distance = 0
    id_cicliste = "ID1_C1"

    config = Config()

    for v in config.global_vars:
        if os.path.exists(v) is False:
            print("Global variable {} is missing. Please read carefully the manual.\n".format(v))
            exit(1)

    file_manager = FileManager(config.get_capture_home())
    microphone = Microphone()
    microphone.set_card_number()
    camera = Camera()
    screen = Screen(port="/dev/ttyUSB2")
    lidar = Lidar(port="/dev/ttyUSB0", _config=config, _screen=screen)
    gps = GPS("/dev/ttyUSB1", 9600, _screen=screen)

    screen.menu()

    while True:
        page_counter = screen.read()
        screen.set_date(get_date())
        screen.set_time(get_time())

        page_counter == b'page2'

        # page 2 /  record
        while page_counter == b'page2':
            screen.clear()
            screen.show_raspberry()

            # Reading input of screen touch nextion (waiting: start)
            while start == b'':
                start = screen.read()
                screen.set_time_recording(get_time())

                # start process of: camera, gps and distance sensor.
                if start == b'start':
                    file_video, file_sound, file_distance, file_gps = file_manager.start_recording(id_cicliste,
                                                                                                   get_date_time_stringify())
                    microphone.start_recording(file_sound)
                    camera.start_recording(file_video)
                    lidar.start_recording(file_distance)
                    gps.start_recording(file_gps)
                    screen.show_recording()
                    # screen.show_microphone()

                    while record is True:
                        stop = screen.read()
                        screen.set_time_recording(get_time())

                        if stop == b'stop':
                            record = False
                            page_counter = b'page2'

                        if stop == b'page1':
                            record = False
                            page_counter = b''

                    microphone.stop_recording()
                    camera.stop_recording()
                    lidar.stop_recording()
                    gps.stop_recording()
                    screen.clear()

                if start == b'page1':  # In/out page1
                    page_counter = b''

            record = True
            start = b''

        while page_counter == b'page3':
            # page 3 (setup)
            format_serial = screen.read()

            if format_serial == b'page1':  # In/out page 2
                page_counter = b''
            elif format_serial == b'in' or format_serial == b'cm':
                config.set_unit(format_serial)

        while page_counter == b'page4':
            # Settings (resolution, distance, export, convert)
            capture_serial = screen.read()
            exporter = None

            try:
                exporter = Exporter()
                screen.set_usb_plug()
            except:
                pass

            if capture_serial == b'page1':
                page_counter = b''
            elif capture_serial == b'capture':
                distance = lidar.set_distance()
                screen.set_distance(distance)
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

        while page_counter == b'page5':
            # page 5  (delete files)
            delete_serial = screen.read()
            if delete_serial == b'page1':
                page_counter = b''
            elif delete_serial == b'delete':
                screen.delete_start()
                try:
                    print("icit")
                    file_manager.delete_files()
                    screen.delete_end()
                    page_counter = b''
                    screen.menu()
                except Exception as error:
                    print(error)
                finally:
                    delete_serial = b''
