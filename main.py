"""
Raspberry project to record distances with vehicules during a bike ride

Conception and hardware: Andres Henao <email@toprovide>
Programming:
    - Andres Henao <email@toprovide>
    - David Maignan <davidmaignan@gmail.com>

Supervisor:
    - Philippe Apparicio <philippe.apparicio@ucs.inrs.ca>

Source code: url to provide
Licence: GPLv3 - https://www.gnu.org/licenses/quick-guide-gplv3.html

"""

import os

from utils.camera import Camera
from utils.gps import GPS
from utils.microphone import Microphone
from utils.videoconverter import VideoConverter
from utils.config import Config
from utils.filemanager import FileManager
from utils.lidar import Lidar
from utils.screen import Screen
from utils.tools import get_date, get_time, get_date_time, get_date_time_stringify

start = b''
record = True
initial_distance = 0  # initial distance
id_cicliste = "ID1_C1"


# def usb_connected():
#     subdirectory = "/media/pi/"
#     # Icon ok for usb connected
#     for root, dirs, files in os.walk(subdirectory):
#         for name in files:
#             if fnmatch.fnmatch(name, '*.txt'):
#                 if name == 'LAEQ.txt':
#                     ser3.write(Usbplug + eof)


if __name__ == '__main__':
    config = Config()

    for v in config.global_vars:
        if os.getenv(v) is None:
            print("Global variable {} is missing. Please read carefully the manual.\n".format(v))
            exit(1)

    # video_converter = VideoConverter()

    file_manager = FileManager(config.get_capture_home())
    microphone = Microphone()
    microphone.set_card_number()
    camera = Camera()
    screen = Screen(port="/dev/ttyUSB2")
    lidar = Lidar(port="/dev/ttyUSB0", config=config)
    gps = GPS("/dev/ttyUSB1", 9600)

    screen.menu()

    while True:
        page_counter = screen.read()
        screen.set_date(get_date())
        screen.set_time(get_time())

        page_counter == b'page2'

        while page_counter == b'page2':  # page 2 /  record
            print("page 2 /  record")
            screen.clear()
            screen.show_raspberry()
            screen.start_recording()

            # Reading input of screen touch nextion (waiting: start)
            while start == b'':
                start = screen.read()
                screen.set_time_recording(get_time())

                # start process of: camera, gps and distance sensor.
                if start == b'start':
                    file_video, file_sound, file_distance, file_gps = file_manager.start(id_cicliste, get_date_time_stringify())
                    microphone.start_recording(file_sound)
                    camera.start_recording(file_video)
                    lidar.start_recording(file_distance)
                    gps.start_recording(file_gps)
                    screen.start_recording()

                    while record is True:
                        stop = screen.read()
                        screen.set_time_recording(get_time())

                        # @todo display distance to screen

                        if stop == b'stop':
                            print("Stop recording")
                            record = False
                            page_counter = b'page2'

                        if stop == b'page1':
                            record = False
                            page_counter = b''

                    microphone.stop_recording()
                    camera.stop_recording()
                    lidar.stop_recording()
                    gps.stop_recording()

                if start == b'page1':  # In/out page1
                    page_counter = b''

            screen.clear()
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

            usb_connected()

            if capture_serial == b'page1':
                page_counter = b''
            elif capture_serial == b'capture':
                distance = lidar.set_distance()
                screen.set_distance(distance)
            elif capture_serial == b'convert':
                screen.convert_start()
                try:
                    screen.convert_end()
                except:
                    convert_files_error()
            elif capture_serial == b'export':
                pass

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
                    file_manager.delete_files()
                    screen.delete_end()
                    page_counter = b''
                    screen.menu()
                finally:
                    delete_serial = b''
