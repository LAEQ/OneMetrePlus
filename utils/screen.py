from multiprocessing.context import Process
from random import random

import serial
import asyncio
import serial_asyncio
import time
import random

from utils.tools import get_time, get_date


class Screen:
    """
        Wrapper to communicate with touch screen connected through usb
        @todo: validate port value
    """
    def __init__(self, port=None):
        self.port = port
        self.serial = serial.Serial(port=port, baudrate=115200,  # ecran
                                      parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                                      bytesize=serial.EIGHTBITS, timeout=0.01)

        self.reader = None
        self.writer = None

        self.eof = b'\xff\xff\xff'
        self._t2 = b't2.txt='  # text object for distance in the record page
        self._t8 = b't8.txt='
        self._t14 = b't14.txt='  # text object for hour in the record page
        self._time = b't15.txt='
        self._date = b't0.txt='

        # Video : red / black circle
        self._P1 = b'p1.pic=0'
        self._P2 = b'p1.pic=2'

        # Raspberry icon / black square
        self._RP1 = b'p3.pic=6'
        self._RP2 = b'p3.pic=2'

        # GPS icon / black square
        self._gp = b'p2.pic=1'
        self._gp2 = b'p2.pic=2'

        # Microphone red / black
        self._Mic = b'p12.pic=32'
        self._Mic2 = b'p12.pic=2'

        self._P4 = b'p4.pic=7'  # image for distance < 100 cm  in the record page (Warning sign)
        self._P42 = b'p4.pic=8'  # image standard for indicator (black square)

        self._dist0 = b'"000"'

        # page number for the animation LAEQ
        self._page0 = b'page 0' + self.eof
        # page number for the main menu
        self._page1 = b'page 1' + self.eof
        # page number for the record page
        self._page2 = b'page 2' + self.eof

        # Gif for delete files
        self._delete = b'va1.val=0'
        self._finish = b'va1.val=1'

        # Convert files
        self._convert = b'va1.val=0'
        self._convert_end = b'va1.val=1'
        self._convert_error = b'p8.pic=36'

        # Export
        self._pexport = b'va3.val=0'
        self._pendexport = b'va3.val=1'
        self._perrorexport = b'p9.pic=36'

        # convert
        self._finishconvert = b'p8.pic=26'
        self._finishexport = b'p9.pic=26'
        self._usbplug = b'p9.pic=31'

    async def set_up(self):
        self.reader, self.writer = await serial_asyncio.open_serial_connection(url=self.port,
                                                                               baudrate=115200,
                                                                               parity=serial.PARITY_NONE,
                                                                               stopbits=serial.STOPBITS_ONE,
                                                                               bytesize=serial.EIGHTBITS,
                                                                               timeout=0.01)

    def read(self):
        return self.serial.readline()

    def menu(self):
        self.serial.write(self._page1)

    def start_recording(self):
        self.serial.write(b'p1.pic=0' + b'\xff\xff\xff')
        # self.serial.write(b'p12.pic=32' + b'\xff\xff\xff')

    def set_time(self, time):
        time = bytes(time, 'utf-8')
        self.serial.write(self._time + time + self.eof)

    def set_date(self, date):
        date = bytes(date, 'utf-8')
        self.serial.write(self._date + date + self.eof)

    def clear(self):
        self.serial.write(self._P2 + self.eof)
        self.serial.write(self._RP2 + self.eof)
        self.serial.write(self._gp2 + self.eof)
        self.serial.write(self._t2 + self._dist0 + self.eof)
        self.serial.write(self._P42 + self.eof)
        self.serial.write(self._Mic2 + self.eof)

    def show_raspberry(self):
        self.serial.write(self._RP1 + self.eof)

    def set_time_recording(self, time):
        time = bytes(time, 'utf-8')
        self.serial.write(self._t14 + time + self.eof)

    def delete_start(self):
        self.serial.write(self._delete + self.eof)

    def delete_end(self):
        self.serial.write(self._finish + self.eof)

    def convert_start(self):
        self.serial.write(self._convert + self.eof)

    def convert_end(self):
        self.serial.write(self._convert_end + self.eof)

    def convert_error(self):
        self.serial.write(self._convert_end + self.eof)
        self.serial.write(self._convert_error + self.eof)

    def set_distance(self, distance):
        distance = b'"%d"' % distance
        self.serial.write(self._t8 + distance + self.eof)

    def export_end(self):
        self.serial.write(self._pendexport + self.eof)
        self.serial.write(self._inishexport + self.eof)

    def export_error(self):
        self.serial.write(self._pendexport + self.eof)
        self.serial.write(self._finishexport + self.eof)

    def set_no_icon(self, distance):
        self.serial.write(self._P42 + self.eof)
        self.serial.write(self._t2 + (b'"%d"' % distance) + self.eof)

    def set_warning(self, distance):
        self.serial.write(self._P4 + self.eof)
        self.serial.write(self._t2 + (b'"%d"' % distance) + self.eof)

    def set_usb_plug(self):
        self.serial.write(self._usbplug + self.eof)

    def write(self, message):
        self.serial.write(message)


if __name__ == "__main__":
    screen = Screen(port="/dev/ttyUSB2")

    while True:
        screen.set_time_recording(get_time())
        screen.set_warning()

        v = random.randint(1,5)

        if v % 2 == 0:
            screen.set_warning()
            screen.write(b'p4.pic=8\xff\xff\xff')
        else:
            screen.set_no_icon()

        time.sleep(1)

# async def main(loop):
#     screen = Screen('/dev/ttyUSB2')
#
#     await screen.set_up()
#
#     sent = send(screen, [])
#     received = recv(screen)
#     await asyncio.wait([sent, received])
#
#
# async def send(_screen, msgs):
#     while True:
#         _screen.set_time(get_time())
#         await asyncio.sleep(1)
#     # # w.write(b'DONE\n')
#     print('Done sending')
#
#
# async def recv(_screen):
#     while True:
#         message = await _screen.reader.read(9)
#         print(message)
#
#
# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main(loop))
#     loop.close()
