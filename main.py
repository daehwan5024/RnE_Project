import cv2
import cv2.aruco as aruco
from djitellopy import tello
import numpy as np
from PID_Controll import controll
import time
import datetime

drone = tello.Tello()
goal_x = 640
goal_y = 360

def findaruco(img, markerSize = 4, totalMarkers=50):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
    arucoDict = aruco.Dictionary_get(aruco.DICT_4X4_50)
    arucoParam = aruco.DetectorParameters_create()
    bboxs, ids, rejected = aruco.detectMarkers(imgGray, arucoDict, parameters=arucoParam)
    return ids, bboxs

def getWhere(bbox):
    print(bbox)
    if(len(bbox)==0):
        return -1, -1
    a = np.reshape(bbox, (2,4))
    return np.sum(a, axis=1)/4


controller = controll(np.array([640, 360]))

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_XI_FRAMERATE, 60.0)


start = time.time()

frames = 0
start = time.time()
while(True):
    ret, img = cap.read()
    if not ret:
        continue
    cv2.imshow('test', img)
    id, bbox = findaruco(img)
    frames = frames+1
    print(controller.get_speed(getWhere(bbox)))

    if (cv2.waitKey(1) & 0xff) == ord('q'):
        break
sec = time.time()-start
cap.release()
print(frames)
print(sec)
print(frames/sec)