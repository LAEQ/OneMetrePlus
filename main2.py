import os
import serial
import asyncio
import serial_asyncio

from utils.app import Application
from utils.camera import Camera
from utils.config import Config
from utils.filemanager import FileManager
from utils.lidar import Lidar
from utils.microphone import Microphone
from utils.screen import Screen


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
                print(message)

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

    global config, file_manager, screen, camera, sound, lidar, gps

    config = Config()

    for v in config.global_vars:
        if os.getenv(v) is None:
            print("Global variable {} is missing. Please read carefully the manual.\n".format(v))
            exit(1)

    screen = Screen("/dev/ttyUSB2")
    file_manager = FileManager(config.get_capture_home())
    camera = Camera()
    microphone = Microphone()
    lidar = Lidar(port="/dev/ttyUSB0")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop, config))
    loop.close()
