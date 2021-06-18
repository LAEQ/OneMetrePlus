import serial
import serial_asyncio


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
        self._page0 = b'page animation' + self.eof
        # page number for the main menu
        self._page1 = b'page home' + self.eof
        # page number for the record page
        self._page2 = b'page record' + self.eof

        # Gif for delete files
        self._delete = b'va1.val=0'
        self._finish = b'va1.val=1'

        # Convert files
        self._convert = b'va1.val=0'
        self._convert_end = b'va1.val=1'
        self._convert_end_green = b'p8.pic=26'
        self._convert_error = b'p8.pic=36'

        # Export
        self._pexport = b'va3.val=0'
        self._pendexport = b'va3.val=1'
        self._pendexport_green = b'p9.pic=26'
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
        self.hide_recording()
        self.hide_raspberry()
        self.hide_gps()
        self.show_distance_null()
        self.hide_warning()

    def show_raspberry(self):
        self.serial.write(self._RP1 + self.eof)

    def hide_raspberry(self):
        self.serial.write(self._RP2 + self.eof)

    def show_microphone(self):
        self.serial.write(self._Mic + self.eof)

    def hide_microphone(self):
        self.serial.write(self._Mic2 + self.eof)

    def show_gps(self):
        self.serial.write(self._gp + self.eof)

    def hide_gps(self):
        self.serial.write(self._gp2 + self.eof)

    def show_recording(self):
        self.serial.write(self._P1 + self.eof)

    def hide_recording(self):
        self.serial.write(self._P2 + self.eof)

    def show_warning(self):
        self.serial.write(self._P4 + self.eof)

    def hide_warning(self):
        self.serial.write(self._P42 + self.eof)

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
        self.serial.write(self._convert_end_green + self.eof)        

    def convert_error(self):
        self.serial.write(self._convert_end + self.eof)
        self.serial.write(self._convert_error + self.eof)

    def export_start(self):
        self.serial.write(self._pexport + self.eof)

    def export_end(self):
        self.serial.write(self._pendexport + self.eof)
        self.serial.write(self._pendexport_green + self.eof)

    def export_error(self):
        self.serial.write(self._pendexport + self.eof)
        self.serial.write(self._perrorexport + self.eof)

    def set_no_icon(self, distance):
        self.serial.write(self._P42 + self.eof)
        self.serial.write(self._t2 + (b'"%d"' % distance) + self.eof)

    def set_warning(self, distance):
        self.show_warning()
        self.show_distance(distance)

    def set_usb_plug(self):
        self.serial.write(self._usbplug + self.eof)

    def write(self, message):
        self.serial.write(message)

    def set_distance(self, distance):
        distance = b'"%d"' % distance
        self.serial.write(self._t8 + distance + self.eof)

    def show_distance(self, distance):
        self.hide_warning()
        self.serial.write(self._t2 + (b'"%d"' % distance) + self.eof)

    def show_warning_distance(self, distance):
        self.show_warning()
        self.serial.write(self._t2 + (b'"%d"' % distance) + self.eof)

    def show_distance_null(self):
        self.hide_warning()
        self.serial.write(self._t2 + self._dist0 + self.eof)

    def show_recording_2(self):
        self.writer.write(self._P1 + self.eof)

    def hide_recording_2(self):
        self.writer.write(self._P2 + self.eof)


if __name__ == "__main__":
    screen = Screen(port="/dev/ttyUSB2")

    screen.menu()




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
