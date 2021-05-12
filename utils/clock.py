import time
import subprocess
import multiprocessing
from datetime import datetime as dt

import asyncio

from utils.screen import Screen


class Clock:
    def __init__(self):
        self.clock_process = None

    def get_time(self) -> str:
        time = dt.now().strftime('%H:%M:%S')
        return '"{}"'.format(time)

    def get_date(self) -> str:
        date = dt.now().strftime('%Y-%m-%d')
        return '"{}"'.format(date)

    def get_date_time(self) -> str:
        return dt.now().strftime('%Y-%m-%d %H:%M:%S')

    def get_date_time_stringify(self):
        return "{}_{}".format(self.get_date(), self.get_time()).replace(":", "_").replace("-", "_").replace('"', '')

    def get_timestamp_milli(self):
        return dt.datetime.now().strftime('%H:%M:%S.%f')

    def clocking(self):
        while True:
            print("clocking")
            time.sleep(3)

    def start_clock(self):
        self.clock_process = multiprocessing.Process(
            target=self.clocking,
            args=()
        )

        self.clock_process.start()

    def stop_clock(self):
        self.clock_process.terminate()
