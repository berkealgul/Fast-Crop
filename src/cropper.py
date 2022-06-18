import cv2


class ROISelector:
    def __init__(self, frame):
        self.activeX = -1
        self.activeY = -1
        self.roi_x = 1
        self.roi_y = 1
        self.roiSelected = False
        self.frame = frame
        cv2.namedWindow('ROI Selection')  
        cv2.setMouseCallback('ROI Selection', self.roiMouseHandler)  

    def roiMouseHandler(self, event, x, y, flags, param):  
        self.activeX = x
        self.activeY = y

        if(event == cv2.EVENT_LBUTTONDBLCLK):  
            print("click")
        elif(event == cv2.EVENT_RBUTTONDBLCLK):  
            pass

    def roiSelection(self, frame):


        while self.roiSelected is False:
            v0 = (self.roi_x, self.roi_y)
            v1 = (self.activeX, self.activeY)
            print(v1)
            cv2.rectangle(frame, v0, v1, (0,255,0), 2)
            cv2.imshow('ROI Selection', frame)
            cv2.waitKey(0)


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
    rs = ROISelector()
    rs.roiSelection(frame)

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