class PeopleCounter:

    def __init__(self, videoMeta, videoStream, frameProcessor):
        self.insideCount = 0
        self.videoMeta = videoMeta
        self.videoStream = videoStream
        self.frameProcessor = frameProcessor

    def resetCounter(self):
        self.insideCount = 0

    def incrementCounter(self):
        self.insideCount = self.insideCount + 1

    def decrementCounter(self):
        self.insideCount = self.insideCount - 1

    def checkAndCountPeople(self, centerPoints):
        xCoordinates = []
        for val in centerPoints:
            xCoordinates.append(val[0])
        outside=[]
        inside=[]
        for xVal in xCoordinates:
            if x > midLine:
                outside.append(x)
            else:
                inside.append(x)
            if len(outside) > 0 and len(inside) > 0:
                break

        if xVal[0] > midLine:
            direction = -1
        else:
            direction = 1

        if len(outside) > 0 and len(inside) > 0:
            if direction == 1:
                self.incrementCounter()
                return 1
            elif direction == -1:
                self.decrementCounter()
                return -1
        return 0

    def findPeople(self, contours):
        people = []
        areas = []
        for c in contours:
            area = cv2.contourArea(c)
            areas.append(area)
            if area >= 300:
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
                print self.insideCount
            else:
                people.append(p)
        return people

    def start(self):
        while(True):
            ret, frame = self.videoStream.read()
            if not ret:
                break
            frame = self.frameProcessor.drawLine(frame)
            frame = self.frameProcessor.subtractBackground(frame)
            frame = self.frameProcessor.applyThreshold(frame)
            frame = self.frameProcessor.blurFrame(frame)
            frame = self.frameProcessor.morphFrame(frame)
            frame = self.frameProcessor.dilateFrame(frame)
            cv2.imshow('ProcessedFrame', frame)
            img, contours, hierarchy = self.frameProcessor.findContours()
            people = updateCount(contours,  people)
            cv2.drawContours(frame, contours, -1, (0,0,255), 3)
            cv2.imshow('cotoured', frame)
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break
        self.videoStream.stop()
