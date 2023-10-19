from gpiozero import Button
import time
from multiprocessing.context import Process

from utils.screen import Screen

class Switch:

    def __init__(self,_screen: Screen):
        self.process = None
        self.file = None
        self.screen = _screen

    def record(self, file_path: str) -> None:
        with open(file_path, "w") as _file:
            _file.write("timeButton\n")
            button = Button(16)
            while True:
                try:                   
                    button.wait_for_press()
                    value = "{}\n".format(time.time())
                    _file.write(value)
                    _file.flush()
                    self.screen.show_switch()
                    time.sleep(1)
                    self.screen.hide_switch() 
                except:
                    pass

    def start_recording(self, file_path: str) -> None:
        self.process = Process(target=self.record, args=(file_path, ))
        self.process.start()

    def stop_recording(self) -> None:
        self.process.terminate()
        self.process.join()



if __name__ == "__main__":
    screen = Screen(port="/dev/ttyUSB2")
    switch = Switch(_screen=screen)
    print("Start")
    file = "button.csv"
    switch.start_recording(file)

    time.sleep(30)
    switch.stop_recording()
    print("End")

    # with open(file, 'r') as f:
    #     line = f.read()
    #     print(line)


