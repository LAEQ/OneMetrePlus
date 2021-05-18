import subprocess
import os
import time


class Stream:
    def __init__(self):
        self.name = "hw:CARD=sndrpii2scard"
        self.card_number = 0
        self.rate = 11025
        self.audio_enconder = "pcm_s32le"
        self.audio_channel = 1
        self.input_format = "h264"
        self.format = "wav"
        self.sample_format = ["S16_LE", "S24_LE", "S32_LE"]
        self.camera_resolution_width=640
        self.camera_resolution_height=360
        self.frame_rate = 25
        self.video_format = "video4linux2"
        self.input_device = "/dev/video0"
        self.streaming_process = None


    def get_streaming_command(self, file):
        return "ffmpeg -y -use_wallclock_as_timestamps 1 -vsync 1 -async 1 " \
               "-ar {} -acodec {} -ac {} -f alsa -i plughw:{} " \
               "-f {} -input_format {} -video_size {}x{} -framerate {} " \
               "-itsoffset 0.5 -thread_queue_size 4096 -i {} -c:v copy -metadata:s:v:0 rotate=0 {}".format(
            self.rate, self.audio_enconder, self.audio_channel, self.card_number, self.video_format, self.input_format,
            self.camera_resolution_width, self.camera_resolution_height, self.frame_rate, self.input_device, file
        )

    def start_streaming(self, file):
        if self.streaming_process is not None and self.streaming_process.poll() is not None:
            self.streaming_process.terminate()

        command = self.get_streaming_command(file)
        args = command.split(" ")
        self.streaming_process = subprocess.Popen(args=args,
                                                  stdout=subprocess.DEVNULL,
                                                  stderr=subprocess.STDOUT,
                                                  close_fds=True)
        # os.system(command)

    def stop_streaming(self):
        self.streaming_process.terminate()
        # pass


if __name__ == "__main__":
    print("Streaming test.")
    stream = Stream()
    file = "test.mp4"
    print("Start streaming")
    stream.start_streaming("/home/pi/captures/video/test_3.mp4")
    time.sleep(30)
    print("End streaming")
    stream.stop_streaming()
