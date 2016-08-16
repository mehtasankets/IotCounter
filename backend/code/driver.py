#!/bin/python

import cv2
import sys
import math
import time
import numpy as np
from person import Person
from videoMeta import VideoMeta
from peopleCounter import PeopleCounter
from frameProcessor import FrameProcessor
from point import Point
from firebaseApi import FirebaseApi
from recordedStream import RecordedStream

p1 = Point(0, 0)
p2 = Point(640, 480)
started = False

def initVideoStream(videoMeta, videoFileName):
    if videoFileName == None:
        from imutils.video.pivideostream import PiVideoStream
        videoStream = PiVideoStream((videoMeta.width, videoMeta.height), videoMeta.framerate).start()
        time.sleep(2.0)
    else:
        videoStream = RecordedStream(videoFileName).start()
        time.sleep(2.0)
    return videoStream

def getRegion(event, x, y, flags, img):
    global p1, p2, started
    if event == cv2.EVENT_LBUTTONDOWN:
	started = True
	p1.update(x, y)
    elif event == cv2.EVENT_MOUSEMOVE:
	if started == True:
	    frame = img.copy()
  	    cv2.rectangle(frame, (p1.x, p1.y), (x, y), (255, 0, 0), 2)
	    cv2.imshow('Configuration', frame)
    elif event == cv2.EVENT_LBUTTONUP:
	started = False
	p2.update(x, y)
	frame = img.copy()
        cv2.rectangle(frame, (p1.x, p1.y), (x, y), (255, 0, 0), 2)
        cv2.imshow('Configuration', frame)

def initFrame(videoStream):
    img = videoStream.read()
    cv2.namedWindow('Configuration')
    cv2.setMouseCallback('Configuration', getRegion, img)
    cv2.imshow('Configuration', img)
    while(True):
	k = cv2.waitKey(1) & 0xFF
	if k == 27:
	    break
    cv2.destroyAllWindows()

def main():
    global p1, p2
    videoFileName = None
    if len(sys.argv) > 1:
        videoFileName = sys.argv[1]
    height = 480
    width = 640
    framerate = 32
    bgHistory = 50
    bgThreshold = 100
    shadowDetection = False
    midLineColor = (0, 0, 255)
    midLineThickness = 5
    threshVal = 127
    threshMaxVal = 255
    kernelsize = (11, 11)
    firebaseConnection = 'https://iotcounter.firebaseio.com'
    videoMeta = VideoMeta(height, width, framerate)
    videoStream = initVideoStream(videoMeta, videoFileName)
    initFrame(videoStream)
    midLine = int((p2.x - p1.x)/2)
    midLineLenght = int(p2.y - p1.y)
    cropFactor = (p1.x, p2.x, p1.y, p2.y)
    frameProcessor = FrameProcessor(midLineColor, midLineThickness, midLine, midLineLenght, cropFactor, bgHistory, bgThreshold, shadowDetection, threshVal, threshMaxVal, kernelsize, p1, p2)
    firebaseApi = FirebaseApi(firebaseConnection)
    peopleCounter = PeopleCounter(videoMeta, videoStream, frameProcessor, firebaseApi)
    peopleCounter.start()

if __name__ == '__main__':
    main()

