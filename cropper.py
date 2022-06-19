import cv2
import numpy as np

WINDOW_WAIT_TIME = 20 # ms

class RoiManager:
    def __init__(self):
        self.activeX = -1
        self.activeY = -1
        self.roiX = -1
        self.roiY = -1
        self.roiW = -1
        self.roiH = -1
        self.roiSelected = False
        self.frame = None

    def setRoi(self, frame):
        self.frame = frame
        while self.roiSelected is False:
            self.selectRoi()
            self.previewRoi()

    def selectRoi(self):
        winName = 'ROI Selection'
        cv2.namedWindow(winName)  
        cv2.setMouseCallback(winName, self.roiMouseHandler)  
        while self.roiSelected is False:
            cv2.waitKey(WINDOW_WAIT_TIME)
        cv2.destroyWindow(winName)

    def roiMouseHandler(self, event, x, y, flags, param):  
        self.activeX = x
        self.activeY = y
        v0 = (self.roiX, self.roiY)
        v1 = (self.activeX, self.activeY)
        frame_ = self.frame.copy()

        cv2.rectangle(frame_, v0, v1, (0,255,0), 1)
        cv2.imshow('ROI Selection', frame_)

        if(event == cv2.EVENT_LBUTTONDBLCLK):  
            self.setRoiVertex()
            print("set")

    def previewRoi(self):
        winName = 'ROI Preview'
        roi = self.crop(self.frame)
        cv2.namedWindow(winName)
        cv2.imshow(winName, roi)

        while True:
            key = cv2.waitKey(WINDOW_WAIT_TIME)
            if key == 81 or key == 113:
                break # accept roi
            elif key == 69 or key == 101:
                # reject roi and reset values
                self.roiSelected = False 
                self.roiX = -1
                self.roiY = -1
                self.roiW = -1
                self.roiH = -1
                break

        cv2.destroyWindow(winName)

    def crop(self, frame):
        return frame[self.roiY:self.roiY+self.roiH, self.roiX:self.roiX+self.roiW]  

    def setRoiVertex(self):
        if self.roiX == -1: # set upper left vertex
            self.roiX = self.activeX
            self.roiY = self.activeY
        elif self.roiW == -1: # set size
            self.roiW = self.activeX - self.roiX
            self.roiH = self.activeY - self.roiY
            self.roiSelected = True


class TimeLapseManager:
    def __init__(self, cap):
        self.cap = cap
        self.videoLength =  int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.videoBeginPos = 0
        self.videoEndPos = self.videoLength
        self.winName = "TimeLapseManager"
        _ , self.videoBeginFrame = cap.read()
        _ , self.videoEndFrame = cap.read()

    def handleFrameSelectionSlider(self, value):
        # slide values are % based hence we gotta calculate the position
        self.videoBeginPos = int(self.videoLength * min((value/100), 1.0))
        self.cap.set(1, self.videoBeginPos)
        _, self.videoBeginFrame = self.cap.read()
        cv2.imshow(self.winName, self.videoBeginFrame)

    def handleTimeLapseSliderBegin(self, value):
        # slide values are % based hence we gotta calculate the position
        self.videoBeginPos = int(self.videoLength * min((value/100), 1.0))
        self.cap.set(1, self.videoBeginPos)
        _, self.videoBeginFrame = self.cap.read()
        self.showTimeLapseFrames()

    def handleTimeLapseSliderEnd(self, value):
        # slide values are % based hence we gotta calculate the position
        self.videoEndPos = int(self.videoLength * min((value/100), 1.0))
        self.cap.set(1, self.videoEndPos)
        _, self.videoEndFrame = self.cap.read()
        self.showTimeLapseFrames()

    # this function makes user selects any frame from video and returns selected frame
    def selectFrameFromVideo(self):
        cv2.namedWindow(self.winName)
        cv2.createTrackbar("Video Position %", self.winName, 0, 100, self.handleFrameSelectionSlider)
        self.handleFrameSelectionSlider(0)

        while True: # q to complete
            key = cv2.waitKey(WINDOW_WAIT_TIME)
            if key == 81 or key == 113:
                break

        cv2.destroyWindow(self.winName)
        return self.videoBeginFrame # return the resulting frame

    def selectTimeLapses(self):
        cv2.namedWindow(self.winName)
        cv2.createTrackbar("Vid Begin", self.winName, 0, 100, self.handleTimeLapseSliderBegin)
        cv2.createTrackbar("Vid End", self.winName, 0, 100, self.handleTimeLapseSliderEnd)
        self.showTimeLapseFrames()

        # space to confirm lapses
        while True: # q to complete
            key = cv2.waitKey(WINDOW_WAIT_TIME)
            if key == 81 or key == 113:
                break
        
        if self.videoBeginPos > self.videoEndPos:
            print("[Time Lapse Manager] Warning: video ending position is smaller than beginning position. It may cause problems")

        cv2.destroyAllWindows()

    # returns vide positions in the format of -> (begin, end)
    def getTimeLapsePositions(self):
        return self.videoBeginPos, self.videoEndPos

    def showTimeLapseFrames(self):
        vidEnd = self.resizeFrame(self.videoBeginFrame) 
        vidBegin = self.resizeFrame(self.videoEndFrame)
        stacked = np.hstack((vidEnd, vidBegin))
        cv2.imshow(self.winName, stacked)

    # downscales the frame by half of current resolution
    # returns resized frame
    def resizeFrame(self, frame):
        width = int(frame.shape[1] * 0.5)
        height = int(frame.shape[0] * 0.5)
        dim = (width, height)
        return cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)


def main():
    cap = cv2.VideoCapture("example.mp4")
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    #writer = cv2.VideoWriter('outpy.mp4', fourcc, fps, (w,h)) 


    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    n = 0

    ret, frame = cap.read()
    #frame = TimeLapseManager(cap).selectFrameFromVideo()
    #rs = RoiManager()
    #rs.setRoi(frame)
    tm = TimeLapseManager(cap)
    tm.selectTimeLapses()
    print(tm.getTimeLapsePositions())

    cv2.imshow("new frame", frame)

    # it will be changed
    return

    while True:

        ret, frame = cap.read()
        
        n+=1
        
        print("%", (n/length)*100)

        if ret is False:
            break
        
        writer.write(rs.crop(frame))

    writer.release()
    cap.release()


if __name__ == "__main__":
    main()