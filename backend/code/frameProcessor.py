import cv2

class FrameProcessor:

    def __init__(self, midLineColor, midLineThickness, midLine, midLineLength, cropFactor, bgHistory, bgThreshold, shadowDetection, threshVal, threshMaxVal, kernelSize, p1, p2):
        self.midLineColor = midLineColor
        self.midLineThickness = midLineThickness
        self.midLine = midLine
        self.midLineLength = midLineLength
        self.cropFactor = cropFactor
        self.backgroundSubtractor = cv2.createBackgroundSubtractorMOG2(bgHistory, bgThreshold, shadowDetection)
        self.threshVal = threshVal
        self.threshMaxVal = threshMaxVal
        self.kernelSize = kernelSize
	self.p1 = p1
	self.p2 = p2

    def drawMidLine(self, frame):
        cv2.line(frame, (self.midLine, 0), (self.midLine, self.midLineLength), self.midLineColor, self.midLineThickness)
        return frame

    def rotateFrame(self, frame):
        frame = cv2.transpose(frame)
        frame = cv2.flip(frame,  0)

    def cropFrame(self, frame):
        return frame[self.p1.y:self.p2.y, self.p1.x:self.p2.x]

    def subtractBackground(self, frame):
        return self.backgroundSubtractor.apply(frame)

    def applyThreshold(self, frame):
        th, threshold = cv2.threshold(frame, self.threshVal, self.threshMaxVal, cv2.THRESH_BINARY)
	return threshold

    def blurFrame(self, frame):
        return cv2.blur(frame, self.kernelSize)

    def morphFrame(self, frame):
        return cv2.morphologyEx(frame, cv2.MORPH_OPEN, self.kernelSize)

    def dilateFrame(self, frame):
        return cv2.dilate(frame, self.kernelSize, iterations=2)

    def findContours(self, frame):
        image, contours, hierarchy = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	return contours
