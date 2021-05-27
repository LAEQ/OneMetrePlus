import asyncio
import serial_asyncio


class Lidar:
    def __init__(self, port=None, baudrate=115200):
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

    async def set_up(self):
        self.reader, _ = await serial_asyncio.open_serial_connection(url=self.port, baudrate=self.baudrate)



    # def record(self, file_path: str) -> None:
    #     with serial.Serial(self.port, self.baudrate, timeout=self.timeout) as ser, open(file_path, "w") as _file:
    #         unit = self.config.unit
    #         initial_distance = self.config.distance_edge
    #         max_distance = self.config.get_max_distance()
    #         warning_distance = self.config.warning_distance
    #
    #         while True:
    #             recv = ser.read(9)
    #             ser.reset_input_buffer()
    #             if recv[0] == 0x59 and recv[1] == 0x59:
    #                 d = ((recv[2] + recv[3] * 256) - initial_distance) * unit
    #
    #                 if 0 < d < max_distance:
    #                     _file.write("{},{}\n".format(time.time(), d))
    #                     _file.flush()
    #
    #                     if d < warning_distance:
    #                         self.screen.show_warning_distance(d)
    #                     else:
    #                         self.screen.show_distance(d)
    #                 else:
    #                     self.screen.show_distance_null()


async def main_lidar(lp) -> None:
    # Instantiate async reader/writer
    await lidar.set_up()

    await asyncio.wait([read_lidar()])


async def read_lidar():
    while True:
        print("Lidar reader")
        message = await lidar.reader.readline()
        print(message)
        asyncio.sleep(5)


if __name__ == "__main__":
    global lidar
    lidar = Lidar("/dev/ttyUSB0", 115200)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_lidar(loop))

    print("Lidar: stop")



