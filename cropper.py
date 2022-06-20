from sys import argv
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

    def getRoiSize(self):
        self.roiW, self.roiH

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
        if self.roiX == -1: # if user dosent select roi, return the original frame
            return frame 
        else:
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
        #self.cap.set(1, self.videoBeginPos) # cap position is not zero it might need to be reset

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


class ArgManager:
    def __init__(self):
        # getting parameters from command-line arguments
        self.inputVid = argv[1]
        self.outVid = argv[-1]

        # if output and input names are the same we change output name 
        # to avoid overiding the original video
        if self.inputVid == self.outVid:
            self.outVid  = self.outVid.split(".")[0] + "-cropped." + self.outVid.split(".")[1]

        # crop and cutting are default stages if user 
        # dosent enter any parameters
        self.crop = True # size cropping
        self.cut = True  # time cutting
        self.selectFrame = True

        if argv.count("-crop") == 0: 
            self.crop = False
        if argv.count("-cut") == 0:
            self.cut = False
        if argv.count("-fs") == 0:
            self.selectFrame = False


# returns opencv capturer and writers
def generateWriter(outputPath, fps, size):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') # we gotta generate fourcc depending of output format
    writer = cv2.VideoWriter(outputPath, fourcc, fps, size) 
    return writer

def main():
    am = ArgManager()
    rm = RoiManager()
    cap = cv2.VideoCapture(am.inputVid)
    tm = TimeLapseManager(cap)

    if am.crop:
        if am.selectFrame:
            refFrame = tm.selectFrameFromVideo()
        else: # get first frame
            cap.set(1,0)
            _, refFrame = cap.read()
        rm.selectRoi(refFrame)
        frameSize = rm.getCropSize()
    else:
        # get default size if not cropping
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frameSize = (w, h)

    if am.cut:
        tm.selectTimeLapses(am.outVid, cap.get(cv2.CAP_PROP_FPS), frameSize)

    start, end = tm.getTimeLapsePositions()
    length = end-start
    cap.set(1, start) # set capture position
    writer = generateWriter()

    # start video processing
    for i in range(start, end):
        ret, frame = cap.read()

        # print percentage in each 10% per because printing is costy
        if(i % 10 == 0):
            print("Video Processing ", int((i/length)*100), "%")

        if ret is False:
            break
        
        writer.write(rm.crop(frame))

    cap.release()
    writer.release()
    

if __name__ == "__main__":
    main()
