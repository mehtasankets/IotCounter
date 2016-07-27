#!/bin/python
import cv2

class Person:
    id = 0
    def __init__(self, id, trackerBlock):
        self.id = id
        self.trackerBlock = trackerBlock
        self.setCenterPoint(trackerBlock)
        self.setTrack(self.centerPoint)

    def setTrack(self,  centerPoint):
        self.track = []
        self.track.append(centerPoint)

    def setCenterPoint(self,  trackerBlock):
        M = cv2.moments(trackerBlock)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        self.centerPoint = (cx, cy)

    def update(self, trackerBlock):
        self.setCenterPoint(trackerBlock)
        self.trackerBlock = trackerBlock
        self.track.append(self.centerPoint)

    def setId(self):
        self.id = Person.id
        Person.id = Person.id + 1

    def __self__(self):
        return str(self.id) + " " + self.trackerBlock + " " + self.centerPoint + " " + self.track
