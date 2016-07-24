import numpy as np
import cv2
import sys
import math

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

cap = cv2.VideoCapture(0)
height = int(cap.get(3))
width = int(cap.get(4))
fgbg = cv2.createBackgroundSubtractorMOG2(50, 100, False)
firstX = int(width/2-10)
secondX = int(width/2+10)
cntUp = 0
cntDown = 0

def checkAndCountPeople(xy):
    xx = []
    for val in xy:
        xx.append(val[0])
    global cntUp, cntDown
    before = []
    inside = []
    after = []
    direction = 0
    for x in xx:
        if x > secondX:
            before.append(x)
        elif x < firstX:
            after.append(x)
        else:
            inside.append(x)
            if len(after) == 0:
                direction = 1
            else:
                direction = -1
    if len(before) > 0 and len(after) > 0 and len(inside) > 0:
        if direction == 1:
            cntUp = cntUp + 1
            return 1
        elif direction == -1:
            cntDown = cntDown + 1
            return -1
    return 0

def findPeople(contours):
    people = []
    areas = []
    for c in contours:
        area = cv2.contourArea(c)
        areas.append(area)
        if area >= 300:
            people.append(Person(-1, c))
    return people

def closestCenterPoint(peopleInCurrentFrame,  peopleInPreviousFrame):
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

def updatePeopleTracker(peopleInPreviousFrame,  peopleInCurrentFrame):
    count = len(peopleInCurrentFrame)
    updatedTracker = []
    for i in range(count):
        if (len(peopleInCurrentFrame) == 0 or len(peopleInPreviousFrame) == 0):
            break
        closestCurr,  closestPrev = closestCenterPoint(peopleInCurrentFrame,  peopleInPreviousFrame)
        peopleInCurrentFrame.remove(closestCurr)
        peopleInPreviousFrame.remove(closestPrev)
        closestPrev.update(closestCurr.trackerBlock)
        updatedTracker.append(closestPrev)

    if len(peopleInCurrentFrame) != 0:
        for p in peopleInCurrentFrame:
            p.setId()
            updatedTracker.append(p)
    return updatedTracker

def updateCount(contours, peopleInPreviousFrame):
    peopleInCurrentFrame = findPeople(contours)
    peopleTracker = updatePeopleTracker(peopleInPreviousFrame,  peopleInCurrentFrame)
    people = []
    for p in peopleTracker:
        direction = checkAndCountPeople(p.track)
        if direction != 0:
            print (cntUp, cntDown)
        else:
            people.append(p)
    #print(len(people))
    return people

xx = []
direction = 0
people = []
while(True):
    ret, frame = cap.read()
    if not ret:
        break
    #frame = frame[500:1100, 1:600]
    #frame = cv2.transpose(frame)
    #frame = cv2.flip(frame,  0)
    cv2.line(frame, (firstX, 0), (firstX, height), (255, 0, 0),5)
    cv2.line(frame, (secondX, 0), (secondX, height), (255, 0, 0),5)
    fgmask = fgbg.apply(frame)
    #cv2.imshow('masked', fgmask)
    th, threshold = cv2.threshold(fgmask, 127, 255, cv2.THRESH_BINARY)
    #cv2.imshow('threshed', threshold)
    blur = cv2.blur(threshold, (11, 11))
    #cv2.imshow('blurred', blur)
    kernel = np.ones((5,5),np.uint8)
    morphed = cv2.morphologyEx(blur, cv2.MORPH_OPEN, kernel)
    #cv2.imshow('morphed', morphed)
    dilated = cv2.dilate(morphed, kernel, iterations=2)
    cv2.imshow('dilated', dilated)
    im2, contours, hierarchy = cv2.findContours(dilated,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    people = updateCount(contours,  people)
    cv2.drawContours(frame, contours, -1, (0,0,255), 3)
    cv2.imshow('cotoured', frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

