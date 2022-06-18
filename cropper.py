import cv2


class RoiSelector:
    def __init__(self, frame):
        self.activeX = -1
        self.activeY = -1
        self.roiX = -1
        self.roiY = -1
        self.roiW = -1
        self.roiH = -1
        self.roiSelected = False
        self.frame = frame
        cv2.namedWindow('ROI Selection')  
        cv2.setMouseCallback('ROI Selection', self.roiMouseHandler)  

        while True:
            cv2.waitKey(45)

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
        elif(event == cv2.EVENT_RBUTTONDBLCLK):  
            pass

    def previewRoi(self):
        cv2.namedWindow('ROI Preview')
        roi = self.cropFrame()

    def cropFrame(self, frame):
        return frame[self.roiY:self.roiY+self.roiH, self.roiX:self.roiX+self.roiW]  

    def setRoiVertex(self):
        if self.roiX == -1: # set upper left vertex
            self.roiX = self.activeX
            self.roiY = self.activeX
        elif self.roiW == -1: # set size
            self.roiW = self.activeX - self.roiX
            self.roiH = self.activeY - self.roiY
        else:
            self.roiSelected = True



def main():

    x = 0
    y = 0
    w = 100
    h = 100

    cap = cv2.VideoCapture("example.mp4")

    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter('outpy.mp4', fourcc, fps, (w,h)) 


    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    n = 0

    ret, frame = cap.read()
    rs = RoiSelector(frame)

    while True:
        ret, frame = cap.read()
        
        n+=1
        
        print("%", (n/length)*100)

        if ret is False:
            break
        
        writer.write(frame[y:y+h, x:x+w])

    writer.release()
    cap.release()

if __name__ == "__main__":
    main()