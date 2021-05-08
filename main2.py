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
    screen = Screen("/dev/ttyUSB2")
    await screen.set_up()

    file_manager = FileManager(config.get_capture_home())
    camera = Camera()
    microphone = Microphone()
    lidar = Lidar(port="/dev/ttyUSB0")
    application = Applicagit tion(config, file_manager, camera, microphone, lidar)

    await asyncio.wait([receive(screen, application, _config)])


async def receive(_screen, _app, _config):
    _screen.menu()
    while True:
        print("Message ?")
        message = await _screen.reader.read(12)

        if message == b'page1':
            print("page 1")
        elif message == b'page2':
            print("Record")
            while message != b'page1':
                print("Action: ")
                message = await _screen.reader.read(12)
                print(message)

        elif message == b'page3':
            # Setup
            print("Set up")
            while message != b'page1':
                message = await _screen.reader.read(12)


        elif message == b'page4':
            # Format
            print("Format page")
            while message != b'page1':
                print("Action: ")
                message = await _screen.reader.read(12)
                print(message)
                # _app.set_up(message)
            # while True and message != 'page1':
            #     message = await _screen.reader.readuntil(10)
            #     message = message.decode("ascii")
            #     print("icit", message)

        elif message == b'page5':
            print("Delete: ")
            while message != b'page1':
                print("Action: ")
                message = await _screen.reader.read(12)
                print(message)



if __name__ == "__main__":

    config = Config()

    for v in config.global_vars:
        if os.getenv(v) is None:
            print("Global variable {} is missing. Please read carefully the manual.\n".format(v))
            exit(1)


    # app = Application()
    # screen = Screen(port="/dev/ttyUSB2")
    # print("Start Screen")
    # loop = asyncio.get_event_loop()
    # loop.run_forever()
    # print('Done')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop, config))
    loop.close()
