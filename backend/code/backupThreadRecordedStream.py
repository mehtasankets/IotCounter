#!/bin/python
import cv2
from threading import Thread

class RecordedStream:
    def __init__(self, videoFileName):
        self.stream = cv2.VideoCapture(videoFileName)
        self.frame = None
        self.stopped = False

    def start(self):
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        while True:
            ret, self.frame = self.stream.read()
            print self.stopped, ret
            if self.stopped or ret == False:
                self.frame = None
                break
        return

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True
