import os


class Config:
    def __init__(self):
        self.global_vars = ["PROJECT_HOME", "CAPTURE_HOME"]
        self.resolutions = [[800, 600], [600, 450], [400, 300]]

        self.gps_period_capture = 300
        self.resolution = None
        self.unit = 1

        self.set_resolution(None)

        self.max_sensor_distance = 300
        self.distance = 0

    def is_valid_width(self, value):
        return value in self.get_camera_widths()

    def get_camera_widths(self):
        return [bytearray(str(resolution[0]), "utf8") for resolution in self.resolutions]

    def camera_resolution(self):
        return self.resolution[0], self.resolution[1]

    def max_distance(self):
        return self.max_sensor_distance * self.unit

    def get_project_home(self):
        return os.getenv(self.global_vars[0])

    def get_capture_home(self):
        return os.getenv(self.global_vars[1])

    def set_resolution(self, value):
        result = self.resolutions[-1]

        try:
            value = int(value.decode('ascii'))
            result = next(filter(lambda resolution: resolution[0] == value, self.resolutions), result)
        except:
            pass
        finally:
            self.resolution = result
            return self.get_resolution()

    def set_unit(self, value):
        if value == b'in':
            self.unit = 0.393701
        else:
            self.unit = 1

    def get_resolution(self):
        return self.resolution[0], self.resolution[1]

    def set_distance(self, distance):
        self.distance = distance
