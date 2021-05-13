import os
import queue
import threading
import time
import random

import serial
from multiprocessing.context import Process

from utils.config import Config
from utils.messenger import Messenger
from utils.screen import Screen
from utils.tools import get_time


class Lidar:
    def __init__(self, _config: Config, _screen: Screen, port=None, baudrate=115200):
        self.config = _config
        self.screen = _screen
        self.port = port
        self.baudrate = baudrate
        self.timeout = 1
        # self.serial = serial.Serial()
        # self.serial.port = port
        # self.serial.baudrate = baudrate
        self.process = None

        self.warning_message = b'p4.pic=7\xff\xff\xff'
        self.warning_no = b'p4.pic=8\xff\xff\xff'
        self.message_dist_null = b't2.txt="000"\xff\xff\xff'

    def set_distance(self) -> int:
        with serial.Serial(self.port, self.baudrate, timeout=self.timeout) as ser:
            result = -1
            read = ser.read(9)
            ser.reset_input_buffer()

            if read[0] == 0x59 and read[1] == 0x59:
                result = ((read[2] + read[3] * 256) * self.config.unit)

            return result

    def record(self, file_path: str) -> None:
        with serial.Serial(self.port, self.baudrate, timeout=self.timeout) as ser, open(file_path, "w") as _file:
            unit = self.config.unit
            initial_distance = self.config.distance
            max_distance = self.config.get_max_distance()

            print(self.screen)

            while True:
                recv = ser.read(9)
                ser.reset_input_buffer()
                if recv[0] == 0x59 and recv[1] == 0x59:
                    d = ((recv[2] + recv[3] * 256) - initial_distance) * unit

                    if 0 < d < max_distance:
                        _file.write("{},{}\n".format(time.time(), d))
                        _file.flush()

                    if 0 < d <= 100:
                        self.screen.set_warning(d)
                    elif 100 < d <= 260:
                        self.screen.set_no_icon(d)
                    else:
                        pass
                        # self.screen.set_di
                        # ser3.write(t2 + dist0 + eof)

    def start_recording(self, file_path: str) -> None:
        self.process = Process(target=self.record, args=(file_path, ))
        self.process.start()

    def stop_recording(self) -> None:
        self.process.terminate()
        self.process.join()


if __name__ == "__main__":
    config = Config()
    screen = Screen(port="/dev/ttyUSB2")
    lidar = Lidar(port="/dev/ttyUSB0", _config=config, _screen=screen)

    print("Start")
    file = "lidar.csv"
    lidar.start_recording(file)

    time.sleep(10)
    lidar.stop_recording()
    print("End")

    # with open(file, 'r') as f:
    #     line = f.read()
    #     print(line)

    if os.path.exists(file):
        os.remove(file)
