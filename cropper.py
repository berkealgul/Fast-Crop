import cv2


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
        self.windowWaitTime = 20 # ms

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
            cv2.waitKey(self.windowWaitTime)
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
            key = cv2.waitKey(self.windowWaitTime)
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
            



def main():
    cap = cv2.VideoCapture("example.mp4")
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter('outpy.mp4', fourcc, fps, (w,h)) 


    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    n = 0

    ret, frame = cap.read()
    rs = RoiManager()
    rs.setRoi(frame)

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