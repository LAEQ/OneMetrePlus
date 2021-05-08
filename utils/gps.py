import time
import serial
from multiprocessing.context import Process


class GPS:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.process = None

    def record(self, file_path: str) -> None:
        with serial.Serial(self.port, self.baudrate) as ser:
            while True:
                data = ser.readline().decode('ascii', errors='replace')
                print(data)

    def start(self, file_path: str) -> None:
        self.process = Process(target=self.record, args=(file_path,))
        self.process.start()

    def stop(self) -> None:
        self.process.terminate()
        self.process.join()


if __name__ == "__main__":
    gps = GPS("/dev/ttyUSB1", 9600)

    print("Start")
    file = "gps.bin"
    gps.start(file)
    time.sleep(10)
    gps.stop()
    print("End")