import os
import time
import serial
from multiprocessing.context import Process
from utils.config import Config
from utils.screen import Screen


class Lidar:
    def __init__(self, _config: Config, _screen: Screen, port=None, baudrate=115200):
        self.config = _config
        self.screen = _screen
        self.port = port
        self.baudrate = baudrate
        self.timeout = 1
        self.process = None

    def read_distance_to_edge(self) -> int:
        with serial.Serial(self.port, self.baudrate, timeout=self.timeout) as ser:
            result = 0
            read = ser.read(9)
            ser.reset_input_buffer()

            if read[0] == 0x59 and read[1] == 0x59:
                result = (read[2] + read[3] * 256)

            return result

    def record(self, file_path: str) -> None:
        with serial.Serial(self.port, self.baudrate, timeout=self.timeout) as ser, open(file_path, "w") as _file:
            unit = self.config.unit
            distance_edge = self.config.distance_edge
            max_distance = self.config.max_distance
            warning_distance = self.config.warning_distance

            while True:
                recv = ser.read(9)
                ser.reset_input_buffer()
                if recv[0] == 0x59 and recv[1] == 0x59:
                    d = ((recv[2] + recv[3] * 256) - distance_edge)

                    if 0 < d < max_distance:
                        _file.write("{},{}\n".format(time.time(), d * unit))
                        _file.flush()

                        if d < warning_distance:
                            self.screen.show_warning_distance(d * unit)
                        else:
                            self.screen.show_distance(d * unit)
                    else:
                        self.screen.show_distance_null()

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
