import os


class Config:
    def __init__(self):
        self.global_vars = ["/home/pi/capteur-henao", "/home/pi/captures"]
        self.resolutions = [[800, 600], [600, 450], [400, 300]]

        self.gps_period_capture = 300
        self.resolution = None
        self.unit = 1

        self.set_resolution(None)
        self.warning_distance = 100
        self.max_distance = 260

        self.max_sensor_distance = 300
        self.distance_edge = 0
        self.frame_rate = 25

    def get_max_distance(self):
        return self.max_sensor_distance * self.unit

    def is_valid_width(self, value):
        return value in self.get_camera_widths()

    def get_camera_widths(self):
        return [bytearray(str(resolution[0]), "utf8") for resolution in self.resolutions]

    def camera_resolution(self):
        return self.resolution[0], self.resolution[1]

    def max_distance(self):
        return self.max_sensor_distance * self.unit

    def get_project_home(self):
        return self.global_vars[0]

    def get_capture_home(self):
        return self.global_vars[1]

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
        print(value)
        if value == b'in':
            self.unit = 0.393701
        else:
            self.unit = 1

    def get_resolution(self):
        return self.resolution[0], self.resolution[1]

    def set_distance_edge(self, distance):
        self.distance_edge = distance
