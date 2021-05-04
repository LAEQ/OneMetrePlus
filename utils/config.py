import os

class Config:
    def __init__(self):
        self.global_vars = ["PROJECT_HOME", "CAPTURE_HOME"]
        self.gps_period_capture = 300
        self.max_sensor_distance = 300
        self.camera_resolution = [480, 270]
        self.unit = 1

    def camera_resolution(self):
        return self.camera_resolution[0], self.camera_resolution[1]

    def max_distance(self):
        return self.max_sensor_distance * self.unit

    def get_project_home(self):
        return os.getenv(self.global_vars[0])

    def get_capture_home(self):
        return os.getenv(self.global_vars[1])