import serial


class Lidar:
    def __init__(self, port=None, baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        # self.serial = serial.Serial()
        # self.serial.port = port
        # self.serial.baudrate = baudrate

    def set_distance(self, config):
        with serial.Serial(self.port, self.baudrate) as ser:
            result = 0
            read = ser.read(9)

            if read[0] == 0x59 and read[1] == 0x59:
                result = ((read[2] + read[3] * 256) * config.unit)

            return result
