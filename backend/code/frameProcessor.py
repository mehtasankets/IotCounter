import cv2

class FrameProcessor:

    def __init__(self, midLineColor, midLineThickness, midLine, midLineLenght, cropFactor, bgHistory, bgThreshold, shadowDetection, threshVal, threshMaxVal, kernelsize):
        self.midLineColor = midLineColor
        self.midLineThickness = midLineThickness
        self.midLine = midLine
        self.midLineLength = midLineLength
        self.cropFactor = cropFactor
        self.backgroundSubtractor = cv2.createBackgroundSubtractorMOG2(bgHistory, bgThreshold, shadowDetection)
        self.threshVal = threshVal
        self.threshMaxVal = threshMaxVal
        self.kernelSize = kernelSize

    def drawMidLine(self, frame):
        cv2.line(frame, (self.midLine, 0), (self.midLine, self.midLineLength), midLineColor, midLineThickness)
        return frame

    def rotateFrame(self, frame):
        frame = cv2.transpose(frame)
        frame = cv2.flip(frame,  0)

    def cropFrame(self, frame):
        return frame[cropFactor[0]:cropFactor[1], cropFactor[2]:cropFactor[3]]

    def subtractBackground(self, frame):
        return backgroundSubtractor.apply(frame)

    def applyThreshold(self, frame):
        return cv2.threshold(frame, self.threshVal, self.threshMaxVal, cv2.THRESH_BINARY)

    def blurFrame(self, frame):
        return cv2.blur(frame, self.kernelSize)

    def morphFrame(self, frame):
        return cv2.morphologyEx(frame, cv2.MORPH_OPEN, self.kernelSize)

    def dilateFrame(self, frame):
        return cv2.dilate(frame, kernel, iterations=2)

    def findContours(self, frame):
        return cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
