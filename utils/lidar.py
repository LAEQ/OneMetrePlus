import os
import time
import serial
from multiprocessing.context import Process

from utils.config import Config


class Lidar:
    def __init__(self, config, port=None, baudrate=115200):
        self.config = config
        self.port = port
        self.baudrate = baudrate
        self.timeout = 1
        # self.serial = serial.Serial()
        # self.serial.port = port
        # self.serial.baudrate = baudrate
        self.process = None

    def set_distance(self) -> int:
        with serial.Serial(self.port, self.baudrate, timeout=self.timeout) as ser:
            result = 0
            read = ser.read(9)

            if read[0] == 0x59 and read[1] == 0x59:
                result = ((read[2] + read[3] * 256) * self.config.unit)

            return result

    def record(self, file_path: str) -> None:
        with serial.Serial(self.port, self.baudrate, timeout=self.timeout) as ser, open(file_path, "w") as _file:
            unit = self.config.unit
            initial_distance = self.config.distance
            while True:
                recv = ser.read(9)
                ser.reset_input_buffer()
                if recv[0] == 0x59 and recv[1] == 0x59:
                    d = ((recv[2] + recv[3] * 256) - initial_distance) * unit
                    _file.write("{},{};".format(time.time(), d))
                    _file.flush()

    def start_recording(self, file_path: str) -> None:
        self.process = Process(target=self.record, args=(file_path,))
        self.process.start()

    def stop_recording(self) -> None:
        self.process.terminate()
        self.process.join()


if __name__ == "__main__":
    config = Config()
    lidar = Lidar(port="/dev/ttyUSB0", config=config)

    print("Start")
    file = "lidar.csv"
    lidar.start_recording(file)
    time.sleep(10)
    lidar.stop_recording()
    print("End")
    time.sleep(1)

    with open(file, 'r') as f:
        line = f.read()
        print(line)

    if os.path.exists(file):
        os.remove(file)
