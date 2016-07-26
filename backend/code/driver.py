#!/bin/python

import numpy as np
from imutils.video.pivideostream import PiVideoStream
import cv2
import sys
import math
from person import Person
from videoMeta import VideoMeta
from peopleCounter import PeopleCounter
from frameProcessor import FrameProcessor

def initVideoStream(videoMeta):
    videoStream = PiVideoStream((videoMeta.width, videoMeta.height), videoMeta.framerate).start()
    time.sleep(2.0)
    return videoStream

def main():
    height = 480
    width = 640
    framerate = 32
    bgHistory = 50
    bgThreshold = 100
    shadowDetection = False
    midLineColor = (0, 0, 255)
    midLineThickness = 5
    midLine = int(width/2)
    midLineLenght = height
    cropFactor = (0, 640, 0, 480)
    threshVal = 127
    threshMaxVal = 255
    kernelsize = (11, 11)
    videoMeta = VieoMeta(height, width, framerate)
    frameProcessor = FrameProcessor(midLineColor, midLineThickness, midLine, midLineLenght, cropFactor, bgHistory, bgThreshold, shadowDetection, threshVal, threshMaxVal, kernelsize)
    peopleCounter = PeopleCounter(videoMeta, videoStream, frameProcessor)
    peopleCounter.start()

if __name__ == '__main__':
    main()

