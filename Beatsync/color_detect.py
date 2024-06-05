import numpy as np
import cv2

def nothing(x):
    pass


def calibrate(key):
    cap= cv2.VideoCapture(0, cv2.CAP_DSHOW)
    #cap = cv.VideoCapture('http://192.168.1.10:4747/mjpegfeed')
    if key=='z':
        with open('BeatSyncCodes/stick_1.txt', 'r') as file:
            L1 = file.readline()
            L2 = file.readline()
        l1= [int(x) for x in L1.split(",")]
        l2= [int(x) for x in L2.split(",")]
        lower = np.array(l1)        # [107, 151, 139]  #[88, 109, 121]#[95, 94, 182]
        upper = np.array(l2)
    if key=='x':
        with open('BeatSyncCodes/stick_2.txt', 'r') as file:
            L1 = file.readline()
            L2 = file.readline()
        l1= [int(x) for x in L1.split(",")]
        l2= [int(x) for x in L2.split(",")]
        lower = np.array(l1)        # [107, 151, 139]  #[88, 109, 121]#[95, 94, 182]
        upper = np.array(l2)
    cv2.namedWindow('Tracking')
    cv2.createTrackbar('LH', 'Tracking',lower[0], 255,nothing)
    cv2.createTrackbar('LS', 'Tracking',lower[1], 255,nothing)
    cv2.createTrackbar('LV', 'Tracking',lower[2], 255,nothing)
    cv2.createTrackbar('UH', 'Tracking',upper[0], 255,nothing)
    cv2.createTrackbar('US', 'Tracking',upper[1], 255,nothing)
    cv2.createTrackbar('UV', 'Tracking',upper[2], 255,nothing)

    while True:
        #frame = cv2.imread('color_balls.jpg')
        _ ,frame=cap.read()

        #hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2YCrCb)
        hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

        l_h = cv2.getTrackbarPos('LH', 'Tracking')
        l_s = cv2.getTrackbarPos('LS', 'Tracking')
        l_v = cv2.getTrackbarPos('LV', 'Tracking')

        u_h = cv2.getTrackbarPos('UH', 'Tracking')
        u_s = cv2.getTrackbarPos('US', 'Tracking')
        u_v = cv2.getTrackbarPos('UV', 'Tracking')

        lower_color=np.array([l_h,l_s,l_v])
        upper_color=np.array([u_h,u_s,u_v])

        mask=cv2.inRange(hsv,lower_color,upper_color)


        res=cv2.bitwise_and(frame,frame, mask=mask)

        cv2.imshow('IMAGE', frame)
        cv2.imshow('MASK', mask)
        cv2.imshow('BIT AND', res)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            if key=='z':
                with open('BeatSyncCodes/stick_1.txt', 'w') as file:
                    file.write(','.join(str(color) for color in lower_color))
                with open('BeatSyncCodes/stick_1.txt', 'a') as file:
                    file.write('\n')
                    file.write(','.join(str(color) for color in upper_color))
            elif key=='x':
                with open('BeatSyncCodes/stick_2.txt', 'w') as file:
                    file.write(','.join(str(color) for color in lower_color))
                with open('BeatSyncCodes/stick_2.txt', 'a') as file:
                    file.write('\n')
                    file.write(','.join(str(color) for color in upper_color))
            cap.release()
            cv2.destroyAllWindows()
            return

def hsv_upper_lower_value():
    with open('BeatSyncCodes/stick_1.txt', 'r') as file:
        L1 = file.readline()
        L2 = file.readline()
    l1= [int(x) for x in L1.split(",")]
    l2= [int(x) for x in L2.split(",")]
    lower_blue = np.array(l1)        # [107, 151, 139]  #[88, 109, 121]#[95, 94, 182]
    upper_blue = np.array(l2)       # [127,120,255][120, 250, 255] #[109, 165, 241]

    with open('BeatSyncCodes/stick_2.txt', 'r') as file:
        L1 = file.readline()
        L2 = file.readline()
    l1= [int(x) for x in L1.split(",")]
    l2= [int(x) for x in L2.split(",")]
    lower_green = np.array(l1)   #[39,102,84]  #[60, 98, 30] #[43, 56, 179]
    upper_green = np.array(l2)  #[84,255,255]  #[93, 255, 255] [71, 165, 226]

    return lower_blue,upper_blue,lower_green,upper_green