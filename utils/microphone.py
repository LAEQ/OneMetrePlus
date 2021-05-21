import subprocess
import os
import time


class Microphone:
    def __init__(self, _rate=25000):
        self.name = "hw:CARD=sndrpii2scard"
        self.card_number = None
        self.rate = _rate
        self.format = "wav"
        self.sample_format = ["S16_LE", "S24_LE", "S32_LE"]

        self.set_card_number()

        self.recording_process = None

    def get_record_command(self):
        return "arecord -D plughw:{} -c1 -r {} -f {} -t {} -V mono".format(
            self.card_number, self.rate, self.get_sample_format(), self.format
        )

    def start_recording(self, file):
        if self.recording_process is not None and self.recording_process.poll() is not None:
            self.recording_process.terminate()

        command = self.get_record_command()
        args = command.split(" ") + [file]
        self.recording_process = subprocess.Popen(args=args,
                                                  stdout=subprocess.DEVNULL,
                                                  stderr=subprocess.STDOUT,
                                                  close_fds=True)

    def stop_recording(self):
        self.recording_process.terminate()

    def get_sample_format(self, index=-1):
        return self.sample_format[index]

    def set_card_number(self):
        result = subprocess.run(["cat", "/proc/asound/cards"], capture_output=True)
        output = result.stdout.decode("utf8").strip()
        output = output.split(" ")
        self.card_number = output[0]


if __name__ == "__main__":
    print("microphone test.")
    microphone = Microphone()
    print("Start recording")
    microphone.start_recording("/home/pi/captures/sound/test.wav")
    time.sleep(10)
    print("End recording")
    microphone.stop_recording()

    # if os.path.exists(file):
    #     print("RECORDING {} found".format(file))
    #     os.remove(file)
    #     print("FILE {} deleted {}".format(file, os.path.exists(file) is False))
    # else:
    #     print("NO RECORDING FILE")

