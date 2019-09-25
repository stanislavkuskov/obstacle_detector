import cv2
import time

from base import BaseThread


class Streamer(BaseThread):

    def __init__(self, src=0):
        super().__init__()
        self.stream = cv2.VideoCapture(src)
        (self.is_grabbed, self.frame) = self.stream.read()
        self.frame_timestamp = .0

    def run(self):
        while not self.is_stopped:
            if not self.is_grabbed:
                self.stop()
            else:
                (self.is_grabbed, self.frame) = self.stream.read()
                self.frame_timestamp = "%.20f" % time.time()

    @property
    def get_frame(self):
        return self.frame

    @property
    def get_frame_and_timestamp(self):
        return self.frame, self.frame_timestamp

    @property
    def get_stream(self):
        return self.stream

    @property
    def get_is_grabbed(self):
        return self.is_grabbed
