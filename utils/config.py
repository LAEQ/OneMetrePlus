import yaml


class Config:
    def __init__(self, file: str):
        with open(file, 'r') as stream:
            self.settings = yaml.safe_load(stream)

        self.project_home = self.settings["project"]["home"]
        self.capture_dir = self.settings["project"]["capture"]
        self.id_cyclist = self.settings["project"]["id_cyclist"]

        # GPS
        self.gps_period_capture = self.settings['gps']['period_capture']

        # Lidar
        self.unit = self.settings['lidar']['unit']['cm']
        self.warning_distance = self.settings['lidar']['distance']['warning']
        self.max_distance = self.settings['lidar']['distance']['max']
        self.distance_edge = 0

        # Camera
        self.frame_rate = self.settings['camera']['frame_rate']
        self.resolution = self.settings['camera']['resolution']['large']

    def get_camera_widths(self):
        widths = [self.settings['camera']['resolution'][key]['width'] for key in self.settings['camera']['resolution']]
        return [bytes(str(value), "utf8") for value in widths]

    def is_valid_width(self, value):
        return value in self.get_camera_widths()

    def get_max_distance(self):
        return self.max_distance * self.unit


    def set_resolution(self, value):
        if value == b'800':
            self.resolution = self.settings['camera']['resolution']['large']
        elif value == b'600':
            self.resolution = self.settings['camera']['resolution']['medium']
        else:
            self.resolution = self.settings['camera']['resolution']['small']

    def set_unit(self, value):
        if value == b'in':
            self.unit = self.settings['lidar']['unit']['inch']
        else:
            self.unit = self.settings['lidar']['unit']['cm']

    def get_resolution(self):
        return self.resolution['width'], self.resolution['height']

    def set_distance_edge(self, distance):
        self.distance_edge = distance

    def get_distance_edge(self):
        return self.distance_edge * self.unit
