import cv2


def main():
    x = 0
    y = 0
    w = 100
    h = 100

    cap = cv2.VideoCapture("example.mp4")

    fw = int(cap.get(3))
    fh = int(cap.get(4))
    fps = 15

    writer = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), fps, (fw,fh)) 

    while True:
        ret, frame = cap.read()
        
        if ret is False:
            break

        writer.write(frame[y:y+h, x:x+w])


if __name__ == "__main__":
    main()