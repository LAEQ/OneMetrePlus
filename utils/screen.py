import serial


class Screen:
    """
        Wrapper to communicate with touch screen connected through usb
        @todo: validate port value
    """
    def __init__(self, port="/dev/ttyUSB2"):
        self.serial = serial.Serial(port=port, baudrate=115200,  # ecran
                                      parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                                      bytesize=serial.EIGHTBITS, timeout=0.01)

        self.eof = b'\xff\xff\xff'
        self._t2 = b't2.txt='  # text object for distance in the record page
        self._t8 = b't8.txt='
        self._t14 = b't14.txt='  # text object for hour in the record page
        self._time = b't15.txt='
        self._date = b't0.txt='

        # Image for recording: red / black circle
        self._P1 = b'p1.pic=0'
        self._P2 = b'p1.pic=2'

        # raspberry connection / black square
        self._RP1 = b'p3.pic=6'
        self._RP2 = b'p3.pic=2'

        # GPS in the record page / black square
        self._gp = b'p2.pic=1'  # image for GPS in the record page (target)
        self._gp2 = b'p2.pic=2'  # image standard for indicator (black square)

        self._Mic = b'p12.pic=32'  # image for microphone in the record page (mic icon)
        self._Mic2 = b'p12.pic=2'  # image standard for indicator (black square)

        self._P4 = b'p4.pic=7'  # image for distance < 100 cm  in the record page (Warning sign)
        self._P42 = b'p4.pic=8'  # image standard for indicator (black square)

        self._dist0 = b'"000"'

        self._page0 = b'page 0'  # page number for the animation LAEQ
        self._page1 = b'page 1'  # page number for the main menu
        self._page2 = b'page 2'  # page number for the record page

    def read(self):
        return self.serial.readline()

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

