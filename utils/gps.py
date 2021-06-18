import time

import pynmea2
import serial
from multiprocessing.context import Process

from utils.screen import Screen


class GPS:
    def __init__(self, port, baudrate, _screen: Screen):
        self.port = port
        self.baudrate = baudrate
        self.screen = _screen
        self.process = None
        self.serial = serial.Serial()
        self.serial.baudrate = self.baudrate
        self.serial.port = self.port
        self.file = None

    def record(self, file_path: str) -> None:
        with serial.Serial(self.port, self.baudrate) as ser, open(file_path, "w") as _file:
            _file.write("time,latitude,longitude\n")
            while True:
                data = ser.readline().decode('ascii', errors='replace')
                if data[1:6] == "GNGGA":
                    try:
                        position = pynmea2.parse(data)
                        value = "{},{},{}\n".format(time.time(), position.latitude, position.longitude)
                        _file.write(value)
                        _file.flush()

                        self.screen.show_gps()

                        if position.latitude == 0:
                            self.screen.hide_gps()
                    except:
                        self.screen.hide_gps()

    def start_recording(self, file_path: str) -> None:
        self.process = Process(target=self.record, args=(file_path,))
        self.process.start()

    def stop_recording(self) -> None:
        self.process.terminate()
        self.process.join()


if __name__ == "__main__":
    screen = Screen(port="/dev/ttyUSB2")
    gps = GPS("/dev/ttyUSB1", 9600, screen)

    print("GPS: start")
    file = "gps_test.csv"
    gps.start_recording(file)
    time.sleep(120)
    gps.stop_recording()
    print("End")
    time.sleep(3)

    with open(file, "r") as f:
        print(f.readline())



    print("GPS: stop")
