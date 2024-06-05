import numpy as np
import cv2

def nothing(x):
    pass



def drumPos():    
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    #cap = cv.VideoCapture('http://192.168.1.10:4747/mjpegfeed')
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2200)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2000)
    cor= [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    with open('BeatSyncCodes/box_boundary.txt', 'r') as file:
        L1 = file.readline()
    coordinates= [int(x) for x in L1.split(",")]

    cv2.namedWindow('Position_b1')
    cv2.createTrackbar('X1_b1', 'Position_b1',coordinates[0], 1600,nothing)
    cv2.createTrackbar('y1_b1', 'Position_b1',coordinates[1], 720,nothing)
    cv2.createTrackbar('X2_b1', 'Position_b1',coordinates[2], 1600,nothing)
    cv2.createTrackbar('Y2_b1', 'Position_b1',coordinates[3], 720,nothing)

    cv2.namedWindow('Position_b2')
    cv2.createTrackbar('X1_b2', 'Position_b2',coordinates[4], 1600,nothing)
    cv2.createTrackbar('y1_b2', 'Position_b2',coordinates[5], 720,nothing)
    cv2.createTrackbar('X2_b2', 'Position_b2',coordinates[6], 1600,nothing)
    cv2.createTrackbar('Y2_b2', 'Position_b2',coordinates[7], 720,nothing)

    cv2.namedWindow('Position_b3')
    cv2.createTrackbar('X1_b3', 'Position_b3',coordinates[8], 1600,nothing)
    cv2.createTrackbar('y1_b3', 'Position_b3',coordinates[9], 720,nothing)
    cv2.createTrackbar('X2_b3', 'Position_b3',coordinates[10], 1600,nothing)
    cv2.createTrackbar('Y2_b3', 'Position_b3',coordinates[11], 720,nothing)

    cv2.namedWindow('Position_b4')
    cv2.createTrackbar('X1_b4', 'Position_b4',coordinates[12], 1600,nothing)
    cv2.createTrackbar('y1_b4', 'Position_b4',coordinates[13], 720,nothing)
    cv2.createTrackbar('X2_b4', 'Position_b4',coordinates[14], 1600,nothing)
    cv2.createTrackbar('Y2_b4', 'Position_b4',coordinates[15], 720,nothing)

    cv2.namedWindow('Position_b5')
    cv2.createTrackbar('X1_b5', 'Position_b5',coordinates[16], 1600,nothing)
    cv2.createTrackbar('y1_b5', 'Position_b5',coordinates[17], 720,nothing)
    cv2.createTrackbar('X2_b5', 'Position_b5',coordinates[18], 1600,nothing)
    cv2.createTrackbar('Y2_b5', 'Position_b5',coordinates[19], 720,nothing)

    

    while True:
        #frame = cv2.imread('color_balls.jpg')
        _ ,frame=cap.read()

        #hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2YCrCb)
        hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

        cor[0] = cv2.getTrackbarPos('X1_b1', 'Position_b1')
        cor[1] = cv2.getTrackbarPos('y1_b1', 'Position_b1')
        cor[2] = cv2.getTrackbarPos('X2_b1', 'Position_b1')
        cor[3] = cv2.getTrackbarPos('Y2_b1', 'Position_b1')

        cor[4] = cv2.getTrackbarPos('X1_b2', 'Position_b2')
        cor[5] = cv2.getTrackbarPos('y1_b2', 'Position_b2')
        cor[6] = cv2.getTrackbarPos('X2_b2', 'Position_b2')
        cor[7] = cv2.getTrackbarPos('Y2_b2', 'Position_b2')

        cor[8] = cv2.getTrackbarPos('X1_b3', 'Position_b3')
        cor[9] = cv2.getTrackbarPos('y1_b3', 'Position_b3')
        cor[10] = cv2.getTrackbarPos('X2_b3', 'Position_b3')
        cor[11] = cv2.getTrackbarPos('Y2_b3', 'Position_b3')

        cor[12] = cv2.getTrackbarPos('X1_b4', 'Position_b4')
        cor[13] = cv2.getTrackbarPos('y1_b4', 'Position_b4')
        cor[14] = cv2.getTrackbarPos('X2_b4', 'Position_b4')
        cor[15] = cv2.getTrackbarPos('Y2_b4', 'Position_b4')

        cor[16] = cv2.getTrackbarPos('X1_b5', 'Position_b5')
        cor[17] = cv2.getTrackbarPos('y1_b5', 'Position_b5')
        cor[18] = cv2.getTrackbarPos('X2_b5', 'Position_b5')
        cor[19] = cv2.getTrackbarPos('Y2_b5', 'Position_b5')

   
        cv2.rectangle(frame, (cor[0],cor[1]), (cor[2],cor[3]), (255, 255, 255), 2)
        cv2.rectangle(frame, (cor[4],cor[5]), (cor[6],cor[7]), (255, 255, 255), 2)
        cv2.rectangle(frame, (cor[8],cor[9]), (cor[10],cor[11]), (255, 255, 255), 2)
        cv2.rectangle(frame, (cor[12],cor[13]), (cor[14],cor[15]), (255, 255, 255), 2)
        cv2.rectangle(frame, (cor[16],cor[17]), (cor[18],cor[19]), (255, 255, 255), 2)

        frame = cv2.flip(frame, 1)
        cv2.imshow('Frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            with open('BeatSyncCodes/box_boundary.txt', 'w') as file:
                    file.write('')
            with open('BeatSyncCodes/box_boundary.txt', 'a') as file:
                    file.write(','.join(str(c) for c in cor))
            cap.release()
            cv2.destroyAllWindows()
            return   

