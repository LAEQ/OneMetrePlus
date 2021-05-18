import os
import serial
import asyncio
import serial_asyncio

from utils.camera import Camera
from utils.config import Config
from utils.filemanager import FileManager
from utils.gps import GPS
from utils.lidar import Lidar
from utils.microphone import Microphone
from utils.screen import Screen
from utils.stream import Stream
from utils.tools import get_date_time_stringify


async def main(lp, _config: Config) -> None:
    # Instantiate async reader/writer
    await screen.set_up()

    await asyncio.wait([read_screen()])


async def read_screen():

    screen.menu()

    while True:
        print("Home ?")
        message = await screen.reader.read(12)
        print("Action: ?")
        if message == b'page2':
            print("Record")
            while message != b'page1':
                message = await screen.reader.read(12)

                if message == b'start':
                    file_video, file_sound, file_distance, file_gps = file_manager.start_recording("V2", get_date_time_stringify())
                    file = file_video.replace("h264", "mp4")
                    print(file)

                    camera.start_ffmpeg_recording(file)
                    lidar.start_recording(file_distance)
                    gps.start_recording(file_gps)
                    screen.show_recording_2()
                else:
                    print("Stop")
                    camera.stop_ffmpeg_recording()
                    gps.stop_recording()
                    lidar.stop_recording()
                    screen.hide_recording_2()


        elif message == b'page3':
            # Setup
            print("Set up")
            while message != b'page1':
                message = await screen.reader.read(12)

        elif message == b'page4':
            # Format
            print("Format page")
            while message != b'page1':
                message = await screen.reader.read(12)
                print(message)

        elif message == b'page5':
            print("Delete: ")
            while message != b'page1':
                message = await screen.reader.read(12)
                print(message)


if __name__ == "__main__":

    global config, file_manager, screen, camera, lidar, gps

    config = Config()

    # for v in config.global_vars:
    #     if os.getenv(v) is None:
    #         print("Global variable {} is missing. Please read carefully the manual.\n".format(v))
    #         exit(1)

    screen = Screen("/dev/ttyUSB2")
    camera = Camera(_config=config)
    file_manager = FileManager(config.get_capture_home())
    # stream = Stream()
    # camera = Camera()
    # microphone = Microphone()
    lidar = Lidar(port="/dev/ttyUSB0", _config=config, _screen=screen)
    gps = GPS("/dev/ttyUSB1", 9600, _screen=screen)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop, config))
    loop.close()
