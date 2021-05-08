import os
import time
import serial
from multiprocessing.context import Process


class Lidar:
    def __init__(self, port=None, baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.timeout = 1
        # self.serial = serial.Serial()
        # self.serial.port = port
        # self.serial.baudrate = baudrate
        self.process = None

    def set_distance(self, unit) -> int:
        with serial.Serial(self.port, self.baudrate, timeout=self.timeout) as ser:
            result = 0
            read = ser.read(9)

            if read[0] == 0x59 and read[1] == 0x59:
                result = ((read[2] + read[3] * 256) * unit)

            return result

    def record(self, file_path: str) -> None:
        unit, initial_distance = 1, 10
        with serial.Serial(self.port, self.baudrate, timeout=self.timeout) as ser, open(file_path, "wb") as file:
            while True:
                recv = ser.read(9)
                ser.reset_input_buffer()
                if recv[0] == 0x59 and recv[1] == 0x59:
                    file.write(recv)
                    # distance = ((recv[2] + recv[3] * 256) * unit) - (initial_distance * unit)
                    # print(distance)

    def start(self, file_path: str) -> None:
        self.process = Process(target=self.record, args=(file_path,))
        self.process.start()

    def stop(self) -> None:
        self.process.terminate()
        self.process.join()


if __name__ == "__main__":
    lidar = Lidar(port="/dev/ttyUSB0")

    print("Start")
    file = "lidar.bin"
    lidar.start(file)
    time.sleep(10)
    lidar.stop()
    print("End")
    time.sleep(1)

    print("File")
    with open(file, 'rb') as f:
        while 1:
            recv = f.read(9)
            if not recv:
                break
            distance = ((recv[2] + recv[3] * 256) * 1) - (10 * 1)
            print(distance)

    if os.path.exists(file):
        os.remove(file)
