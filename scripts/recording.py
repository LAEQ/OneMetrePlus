from __future__ import print_function, division

import time
import os

from utils.camera import Camera
from utils.microphone import Microphone

# def test():
#     command = "ffmpeg -f video4linux2 -input_format h264 -video_size 1280x720 -framerate 30 -i /dev/video0 -vcodec copy -an test.h264"
#     os.system(command)
#
# def test2():
#     command = "ffmpeg -f video4linux2 -input_format h264 -video_size 1280x720 -framerate 30 -i /dev/video0 -vcodec copy -an test.h264"
#     os.system(command)


if __name__ == "__main__":
    print("microphone test.")
    # microphone = Microphone()
    # microphone.start_recording("/home/pi/captures/sound/video.wav".)
    # microphone.stop_recording()

    camera = Camera(_config=None)

    print("Start recording")

    camera.start_ffmpeg_recording("/home/pi/captures/video/video.mp4")

    time.sleep(10)

    camera.stop_ffmpeg_recording()

    print("End recording")


    # command = 'arecord -D plughw:1 -c1 -r 11025 -f S32_LE -t wav -V mono ' + test.wav
    # video_thread = threading.Thread(target=self.record)
    # video_thread.start()

    # camera = Camera()
    # microphone = Microphone()
    # config = Config()
    #
    # video_file = "test.h264"
    #
    # print("Start recording")
    # camera.start_ffmpeg_recording(video_file)
    # microphone.start_recording(sound_file)
    #
    # time.sleep(60)
    # sound_file = "test.wav"
    #
    # camera.set_conf

    # camera.stop_ffmpeg_recording()
    # microphone.stop_recording()
    #
    # cap = cv2.VideoCapture("/dev/video0")
    #
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
    #
    # while cap.isOpened():
    #     ret, frame = cap.read()
    #     if ret:
    #         frame = cv2.flip(frame, 0)
    #         out.write(frame)
    #
    #         if cv2.waitKey(1) & 0xFF == ord('q'):
    #             break
    #
    # cap.release()
    # out.release()

    print("Stop Recording")


