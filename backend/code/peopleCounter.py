import cv2
import numpy as np
from person import Person
import math
import time

class PeopleCounter:

    def __init__(self, videoMeta, videoStream, frameProcessor, firebaseApi):
	self.people = []
        self.insideCount = 0
        self.total = 0
        self.videoMeta = videoMeta
        self.videoStream = videoStream
        self.frameProcessor = frameProcessor
        self.firebaseApi = firebaseApi
        self.currDate = time.strftime("%Y%m%d")

    def resetCounter(self):
        self.insideCount = 0
        self.total = 0

    def checkAndResetCounter(self):
        now = time.strftime("%Y%m%d")
        if now > self.currDate:
            resetCounter(self)
            self.currDate = now
            return True
        return False

    def incrementCounter(self, incrBy):
        self.checkAndResetCounter()
	print str(incrBy) + ' person walked in.'
        self.total = self.total + incrBy
        self.firebaseApi.setTotal(self.total)
        self.firebaseApi.setCounter(self.insideCount)

    def decrementCounter(self, decrBy):
        if(self.checkAndResetCounter()):
            self.firebaseApi.setTotal(self.total)
	print str(decrBy) + ' person walked out.'
        self.insideCount = self.insideCount - decrBy
	if(self.insideCount < 0):
	    self.insideCount = 0
        self.firebaseApi.setCounter(self.insideCount)

    def getPersonCount(self, person):
	x,y,w,h = cv2.boundingRect(person.trackerBlock)
	#print 'width ', w, ' height', h
	personCount = math.floor(h / 180);
	return int(personCount)

    def checkAndCountPeople(self, centerPoints, person):
        xCoordinates = []
	midLine = self.frameProcessor.midLine
        for val in centerPoints:
            xCoordinates.append(val[0])
        outside=[]
        inside=[]
        for xVal in xCoordinates:
            if xVal > midLine:
                outside.append(xVal)
            else:
                inside.append(xVal)
            if len(outside) > 0 and len(inside) > 0:
                break

        if xCoordinates[0] > midLine:
            direction = -1
        else:
            direction = 1

        if len(outside) > 0 and len(inside) > 0:
	    personCount = self.getPersonCount(person)
            if direction == 1:
                self.incrementCounter(personCount)
                return 1
            elif direction == -1:
                self.decrementCounter(personCount)
                return -1
        return 0

    def findPeople(self, contours):
        people = []
        for c in contours:
            area = cv2.contourArea(c)
            if area >= 28000:
                people.append(Person(-1, c))
        return people

    def closestCenterPoint(self, peopleInCurrentFrame,  peopleInPreviousFrame):
        closest = None
        pair = None
        for pc in peopleInCurrentFrame:
            pt1 = pc.centerPoint
            for pp in peopleInPreviousFrame:
                pt2 = pp.centerPoint
                distance = math.hypot(pt2[0] - pt1[0],  pt2[1] - pt1[1])
                if(closest is None or closest > distance):
                    closest = distance
                    pair = (pc,  pp)
        return pair

    def updatePeopleTracker(self, peopleInPreviousFrame,  peopleInCurrentFrame):
        count = len(peopleInCurrentFrame)
        updatedTracker = []
        for i in range(count):
            if (len(peopleInCurrentFrame) == 0 or len(peopleInPreviousFrame) == 0):
                break
            closestCurr,  closestPrev = self.closestCenterPoint(peopleInCurrentFrame,  peopleInPreviousFrame)
            peopleInCurrentFrame.remove(closestCurr)
            peopleInPreviousFrame.remove(closestPrev)
            closestPrev.update(closestCurr.trackerBlock)
            updatedTracker.append(closestPrev)

        if len(peopleInCurrentFrame) != 0:
            for p in peopleInCurrentFrame:
                p.setId()
                updatedTracker.append(p)
        return updatedTracker

    def updateCount(self, contours, peopleInPreviousFrame):
        peopleInCurrentFrame = self.findPeople(contours)
        peopleTracker = self.updatePeopleTracker(peopleInPreviousFrame,  peopleInCurrentFrame)
        people = []
        for p in peopleTracker:
            direction = self.checkAndCountPeople(p.track, p)
            if direction == 0:
                people.append(p)
        return people

    def start(self):
        while(True):
            origframe = self.videoStream.read()
            if origframe is None:
                self.videoStream.stop()
                break
            origframe = self.frameProcessor.cropFrame(origframe)
            origframe = self.frameProcessor.drawMidLine(origframe)
	    cv2.imshow('frame', origframe)
            frame = self.frameProcessor.subtractBackground(origframe)
            frame = self.frameProcessor.applyThreshold(frame)
            frame = self.frameProcessor.blurFrame(frame)
            frame = self.frameProcessor.morphFrame(frame)
            frame = self.frameProcessor.dilateFrame(frame)
            #cv2.imshow('ProcessedFrame', frame)
            contours = self.frameProcessor.findContours(frame)
	    areas = []
            for c in contours:
                area = cv2.contourArea(c)
		if area > 28000:
			areas.append(c)
            self.people = self.updateCount(contours,  self.people)
            cv2.drawContours(origframe, areas, -1, (0,0,255), 3)
            #cv2.imshow('cotoured', origframe)
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break
        self.videoStream.stop()
