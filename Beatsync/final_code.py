import numpy as np
import cv2 as cv
import pygame
import pygame.camera

pygame.mixer.pre_init()
pygame.init()
pygame.camera.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

from color_detect import calibrate
from color_detect import hsv_upper_lower_value
from customize_box import drumPos

cap = cv.VideoCapture(0,cv.CAP_DSHOW)
#cap = cv.VideoCapture('http://192.168.1.10:4747/mjpegfeed')
cap.set(cv.CAP_PROP_FRAME_WIDTH, 2200)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 2000)
print(cv.__version__)
print(cap.get(cv.CAP_PROP_FRAME_WIDTH),cap.get(cv.CAP_PROP_FRAME_HEIGHT))
imageSize = (cap.get(cv.CAP_PROP_FRAME_WIDTH),cap.get(cv.CAP_PROP_FRAME_HEIGHT))

blue = (255, 255, 0)
yellow = (0, 255, 255)
red = (0, 0, 255)
green = (0, 255, 0)
temp = (255,0,255)

color = [blue, yellow, red, green,temp]

floor_tom = pygame.mixer.Sound('drum sound/Floor-Tom-Drum-Hit.mp3')
bass_drum = pygame.mixer.Sound('drum sound/Bass-Drum-Hit.mp3')
hihat_c = pygame.mixer.Sound('drum sound/Hi-Hat-Closed-2.mp3')
hihat_o = pygame.mixer.Sound('drum sound/Hi-Hat-Open-Hit.mp3')
snare = pygame.mixer.Sound('drum sound/Snare-Drum-Hit.mp3')

lower_blue,upper_blue,lower_green,upper_green = hsv_upper_lower_value()

with open('BeatSyncCodes/box_boundary.txt', 'r') as file:
    Line = file.readline()
cor= [int(x) for x in Line.split(",")]
#1000,300,1200,500,780,500,980,700,560,500,760,700,340,500,540,700,120,300,320,500
floorCoords = (cor[0], cor[1], cor[2], cor[3])
bassCoords = (cor[4], cor[5], cor[6], cor[7])
snareCoords = (cor[8], cor[9], cor[10], cor[11])
hihatcCoords = (cor[12], cor[13], cor[14], cor[15])
hihatoCoords = (cor[16], cor[17], cor[18], cor[19])

class sticks(object):
    def __init__(self, color):
        _, self.frame = cap.read()
        self.kernal = np.ones((5, 5), np.uint8)
        self.color = color
        if self.color == "red":
            self.lower = lower_blue
            self.upper = upper_blue
        elif self.color == "blue":
            self.lower = lower_green
            self.upper = upper_green
        self.last5Centers = [(0,0),(0,0),(0,0),(0,0),(0,0)]
        self.wasInSnare = False
        self.wasInfloor = False
        self.wasInbass = False
        self.wasInHihatc = False
        self.wasInHihato = False
        self.delta = 0
    
    def rect(self,frame):
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv, self.lower, self.upper)
        mask = cv.erode(mask, self.kernal, iterations=1)
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, self.kernal)
        mask = cv.dilate(mask, self.kernal, iterations=1)
        cv.imshow(self.color, mask)

        x, y = 0, 0
        self.center, radius = (0,0), 0

        contours, hirarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        try:
            for i in range(10):
                center, radius = cv.minEnclosingCircle(contours[i])
                x, y, r= int(center[0]), int(center[1]), int(radius)
                self.center = (x,y)
                if cv.contourArea(contours[i]) > 2000:
                    cv.circle(frame, (x, y), 10, (0, 255, 255), 3)
                    cv.circle(frame, (x,y), r,(0,0,255),5)
                    self.appendCentersList()
                    self.playSounds()
                    break
        except:
            pass

    def appendCentersList(self):
        self.last5Centers.append(self.center)
        self.last5Centers.pop(0)

    

    def snareHit(self):
        center = self.center
        if self.inDrumZone(center, "snare"):
            if self.wasInSnare == False:
                self.wasInSnare = True
                return True
            else:
                return False
        else:
            self.wasInSnare = False
            return False

    def floorHit(self):
        center = self.center
        if self.inDrumZone(center, "floor"):
            if self.wasInfloor == False:
                self.wasInfloor = True
                return True
            else:
                return False
        else:
            self.wasInfloor = False
            return False

    def bassHit(self):
        center = self.center
        if self.inDrumZone(center, "bass"):
            if self.wasInbass == False:
                self.wasInbass = True
                return True
            else:
                return False
        else:
            self.wasInbass = False
            return False

    def hihatcHit(self):
        center = self.center
        if self.inDrumZone(center, "hihatc"):
            if self.wasInHihatc == False:
                self.wasInHihatc = True
                return True
            else:
                return False
        else:
            self.wasInHihatc = False
            return False
    
    def hihatoHit(self):
        center = self.center
        if self.inDrumZone(center, "hihato"):
            if self.wasInHihato == False:
                self.wasInHihato = True
                return True
            else:
                return False
        else:
            self.wasInHihato = False
            return False


    def inDrumZone(self, center, drum):
        if drum == "bass":
            if (center[0] > bassCoords[0] and center[1] > bassCoords[1] and
                center[0] < bassCoords[2] and center[1] < bassCoords[3]):
                return True
            else:
                return False
        elif drum == "floor":
            if (center[0] > floorCoords[0] and center[1] > floorCoords[1] and
                center[0] < floorCoords[2] and center[1] < floorCoords[3]):
                return True
            else:
                return False
        elif drum == "snare":
            if (center[0] > snareCoords[0] and center[1] > snareCoords[1] and
                center[0] < snareCoords[2] and center[1] < snareCoords[3]):
                return True
            else:
                return False
        elif drum == "hihatc":
            if (center[0] > hihatcCoords[0] and center[1] > hihatcCoords[1] and
                center [0] < hihatcCoords[2] and center[1] < hihatcCoords[3]):
                return True
            else:
                return False
        elif drum == "hihato":
            if (center[0] > hihatoCoords[0] and center[1] > hihatoCoords[1] and
                center [0] < hihatoCoords[2] and center[1] < hihatoCoords[3]):
                return True
            else:
                return False
            
        
    def playSounds(self):
        if self.snareHit():
            self.snareH = True
            self.lastDrumHitCenter = self.center
            loudness = self.determineVolume()
            snare.set_volume(loudness)
            snare.play()
        elif self.floorHit():
            self.floorH = True
            self.lastDrumHitCenter = self.center
            loudness = self.determineVolume()
            floor_tom.set_volume(loudness)
            floor_tom.play()
        elif self.bassHit():
            self.tom2H = True
            self.lastDrumHitCenter = self.center
            loudness = self.determineVolume()
            bass_drum.set_volume(loudness)
            bass_drum.play()
        elif self.hihatcHit():
            self.hihatcH = True
            self.lastDrumHitCenter = self.center
            loudness = self.determineVolume()
            loudness *= 100
            hihat_c.set_volume(loudness)
            hihat_c.play()
        elif self.hihatoHit():
            self.hihatoH = True
            self.lastDrumHitCenter = self.center
            loudness = self.determineVolume()
            loudness *= 100
            hihat_o.set_volume(loudness)
            hihat_o.play()


        
    def findDelta(self):
        self.delta = abs(self.last5Centers[-1][1] - self.last5Centers[-2][1])

    def determineVolume(self):
        volumeConstant = float(self.delta)/100
        if volumeConstant > 1.0:
            volumeConstant = 1.0
        return volumeConstant
    


class App(object):
    def __init__(self):
        self.startScreen = pygame.display.set_mode(imageSize, 0)
        self.redStick = sticks("red")
        self.blueStick = sticks("blue")
        self.currentHelpScreen = 1
        self.videoFont = cv.FONT_HERSHEY_DUPLEX
        self.xFont = 1000
        self.yFont = 30

    def startApp(self):
        pygame.display.set_caption("BeatSync")
        self.mainScreen()
        

    def mainScreen(self):
        screen = self.startScreen

        s1 = pygame.image.load("Screens/1.jpg")
        s2 = pygame.image.load("Screens/2.jpg")
        s3 = pygame.image.load("Screens/3.jpg")
        s4 = pygame.image.load("Screens/4.jpg")
        s5 = pygame.image.load("Screens/5.jpg")
        s6 = pygame.image.load("Screens/6.jpg")
        s7 = pygame.image.load("Screens/7.jpg")
        s8 = pygame.image.load("Screens/8.jpg")
        s9 = pygame.image.load("Screens/9.jpg")
        s10 = pygame.image.load("Screens/10.jpg")
        s11 = pygame.image.load("Screens/11.jpg")
        s12 = pygame.image.load("Screens/12.jpg")
        screenFrame = 0
        screenFrames = [s1, s2, s3, s4,s5,s6,s7,s8,s9,s10,s11,s12]
        while True:
            pygame.time.delay(200)
            screen.blit(screenFrames[screenFrame], (0, 0))
            #screen.blit(whiteDrums, (450, 125))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        self.runHelpScreen()
                    else:
                        pygame.mixer.stop()
                        pygame.display.quit()
                        self.runVideo()
            pygame.display.flip()
            screenFrame += 1
            screenFrame %= 12


    def runHelpScreen(self):
        screen = self.startScreen
        helpScreen1 = pygame.image.load("Screens/help screen1.png")
        helpScreen2 = pygame.image.load("Screens/help screen2.png")
        helpScreen3 = pygame.image.load("Screens/help screen3.png")
        if self.currentHelpScreen == 1:
            screen.blit(helpScreen1, (0, 0))
        elif self.currentHelpScreen == 2:
            screen.blit(helpScreen2, (0, 0))
        elif self.currentHelpScreen == 3:
            screen.blit(helpScreen3, (0, 0))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.currentHelpScreen += 1
                    if self.currentHelpScreen == 4:
                        self.currentHelpScreen = 1
                        self.mainScreen()
                    self.runHelpScreen()
            pygame.display.flip()

    def options(self):
        global lower_blue,upper_blue,lower_green,upper_green,cor,floorCoords,bassCoords,snareCoords,hihatcCoords,hihatoCoords
        screen = self.optionscreen
        option = pygame.image.load("Screens/options.png")
        screen.blit(option, (0, 0))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        calibrate('z')
                        lower_blue,upper_blue,lower_green,upper_green = hsv_upper_lower_value()
                        self.__init__()
                        self.options()
                    elif event.key == pygame.K_x:
                        calibrate('x')
                        lower_blue,upper_blue,lower_green,upper_green = hsv_upper_lower_value()
                        self.__init__()
                        self.options()
                    elif event.key == pygame.K_b:
                        drumPos()
                        with open('BeatSyncCodes/box_boundary.txt', 'r') as file:
                            Line = file.readline()
                        cor= [int(x) for x in Line.split(",")]
                        floorCoords = (cor[0], cor[1], cor[2], cor[3])
                        bassCoords = (cor[4], cor[5], cor[6], cor[7])
                        snareCoords = (cor[8], cor[9], cor[10], cor[11])
                        hihatcCoords = (cor[12], cor[13], cor[14], cor[15])
                        hihatoCoords = (cor[16], cor[17], cor[18], cor[19])
                        self.options()
                    else:
                        pygame.mixer.stop()
                        pygame.display.quit()
                        cap = cv.VideoCapture(0,cv.CAP_DSHOW)
                        #cap = cv.VideoCapture('http://192.168.1.10:4747/mjpegfeed')
                        cap.set(cv.CAP_PROP_FRAME_WIDTH, 2200)
                        cap.set(cv.CAP_PROP_FRAME_HEIGHT, 2000)
                        self.runVideo()
                        break
        
    def runVideo(self):
        frameCount = 0
        x = self.xFont
        y = self.yFont
        font = self.videoFont
        global lower_blue,upper_blue,lower_green,upper_green

        i = 2
        cap = cv.VideoCapture(0,cv.CAP_DSHOW)
        #cap = cv.VideoCapture('http://192.168.1.10:4747/mjpegfeed')
        while True:
            if i %2 == 0:
                _, frame = cap.read()
                
                self.redStick.rect(frame)
                self.blueStick.rect(frame)

                self.redStick.findDelta()
                self.blueStick.findDelta()

                global cor
                cv.rectangle(frame, (cor[0],cor[1]), (cor[2],cor[3]), color[4], 2)
                cv.rectangle(frame, (cor[4],cor[5]), (cor[6],cor[7]), color[3], 2)
                cv.rectangle(frame, (cor[8],cor[9]), (cor[10],cor[11]), color[0], 2)
                cv.rectangle(frame, (cor[12],cor[13]), (cor[14],cor[15]), color[1], 2)
                cv.rectangle(frame, (cor[16],cor[17]), (cor[18],cor[19]), color[2], 2)

                frame = cv.flip(frame, 1)
                frame = cv.putText(frame,'Press q to terminate.', (10, 30), font, 0.75, (143, 35, 71), 2, cv.LINE_4)
                frame = cv.putText(frame,'Press o for options.', (x, y), font, 0.75, (143, 35, 71), 2, cv.LINE_4)
                frame = cv.putText(frame,'Current Velocities:', (x, y+50), font, 0.75, (143, 35, 71), 2, cv.LINE_4)
                frame = cv.putText(frame,str(self.redStick.delta), (x, y+100), font, 0.75, (0, 0, 255), 2, cv.LINE_4)
                frame = cv.putText(frame,str(self.blueStick.delta), (x+100, y+100), font, 0.75, (255, 0, 0), 2, cv.LINE_4)
                cv.imshow('Frame', frame)

                pressedKey = cv.waitKey(1)
                if pressedKey == ord('q'):
                    cv.destroyAllWindows()
                    pygame.quit()
                    exit()
                    break
                elif pressedKey == ord('o'):
                    cap.release()
                    cv.destroyAllWindows()
                    self.optionscreen = pygame.display.set_mode(imageSize, 0)
                    pygame.display.set_caption("BeatSync")
                    self.options()
                frameCount += 1

drums = App()
drums.startApp()
