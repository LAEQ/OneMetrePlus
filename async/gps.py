import time

import asyncio
import pynmea2
import serial
from multiprocessing.context import Process

import serial_asyncio


class GPS:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.process = None
        self.file = None
        self.reader = None

    async def set_up(self):
        self.reader, _ = await serial_asyncio.open_serial_connection(url=self.port, baudrate=self.baudrate)

    def record(self, file_path: str) -> None:
        with serial.Serial(self.port, self.baudrate) as ser, open(file_path, "w") as _file:
            while True:
                data = ser.readline().decode('ascii', errors='replace')
                if data[1:6] == "GNGGA":
                    try:
                        position = pynmea2.parse(data)
                        value = "{},{},{}\n".format(time.time(), position.latitude, position.longitude)
                        _file.write(value)
                        _file.flush()

                        if position.latitude == 0:
                            self.screen.hide_gps()
                        else:
                            self.screen.show_gps()
                    except:
                        pass

    def start_recording(self, file_path: str) -> None:
        self.process = Process(target=self.record, args=(file_path,))
        self.process.start()

    def stop_recording(self) -> None:
        self.process.terminate()
        self.process.join()


async def main_gps(lp) -> None:
    # Instantiate async reader/writer
    await gps.set_up()

    await asyncio.wait([read_gps()])


async def read_gps():
    while True:
        print("GPS reader")
        message = await gps.reader.readline()
        print(message)
        asyncio.sleep(5)


if __name__ == "__main__":
    global gps
    gps = GPS("/dev/ttyUSB1", 9600)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_gps(loop))



    print("GPS: stop")
