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
                    camera.start_recording(file_video)
                    microphone.start_recording(file_sound)
                    lidar.start_recording(file_distance)
                    gps.start_recording(file_gps)

                    screen.show_recording_2()
                else:
                    print("Stop")
                    camera.stop_recording()
                    microphone.stop_recording()
                    lidar.stop_recording()
                    gps.stop_recording()
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

    global config, file_manager, screen, camera, microphone, lidar, gps

    config = Config()

    screen = Screen("/dev/ttyUSB2")
    file_manager = FileManager(config.capture_dir)

    microphone = Microphone(_rate=25000)
    microphone.set_card_number()

    camera = Camera(_config=config)
    camera.camera.rotation = 180

    lidar = Lidar(port="/dev/ttyUSB0", _config=config, _screen=screen)
    gps = GPS("/dev/ttyUSB1", 9600, _screen=screen)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop, config))
    loop.close()
