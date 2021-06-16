import cv2
import cv2.aruco as aruco
from djitellopy import tello
import numpy as np
from PID_Controll import controll
import time

drone = tello.Tello()
drone.connect()
print(drone.get_battery())
drone.send_rc_control(0,0,0,0)

goal = np.array([640, 360])


def findaruco(img, markerSize = 4, totalMarkers=50):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #회색 이미지로 변환
    key = getattr(aruco,
                  f'DICT_{markerSize}X{markerSize}_{totalMarkers}') #필요한 ArUco 마커 Dictionary이름 생성
    arucoDict = aruco.Dictionary_get(key) #ArUco Dictionary 생성
    arucoParam = aruco.DetectorParameters_create() #오차 보정을 위한 파라미터 생성
    bboxs, ids, rejected = aruco.detectMarkers(imgGray, arucoDict,
                                               parameters=arucoParam) #imgGray에서 ArUco 마커 탐색
    return ids, bboxs

def getWhere(bbox):
    print(bbox)
    if(len(bbox)==0):
        return -1, -1
    a = np.reshape(bbox, (2, 4))
    return np.sum(a, axis=1)/4




cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30.0)

controller = controll(goal, np.array([1, 0.3, 0.2]), 1/cap.get(cv2.CAP_PROP_FPS))

frames = 0
start = time.time()
while True:
    ret, img = cap.read()
    frames = frames+1
    if not ret:
        continue
    cv2.imshow('test', img)
    id, bbox = findaruco(img)
    print(controller.get_speed(getWhere(bbox)))

    if (cv2.waitKey(1) & 0xff) == ord('q'):
        break
sec = time.time()-start
cap.release()
