import subprocess
import shutil
import os

from utils.config import Config
from utils.filemanager import FileManager


class Exporter:
    def __init__(self):
        command = "lsblk -l | grep pi | tr -s ' ' | cut -d ' ' -f 7"
        result = subprocess.check_output(command, shell=True)
        self.mount_point = result.decode().strip()

        if result == b'':
            raise Exception("No usb found")

    def export(self, _manager: FileManager):
        dest_folder = os.path.join(self.mount_point, "export")
        shutil.copytree(_manager.export_path(), dest_folder)


if __name__ == "__main__":
    config = Config()
    manager = FileManager(config.capture_dir)
    export = Exporter()
    export.export(manager)
