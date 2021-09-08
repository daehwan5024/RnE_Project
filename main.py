import cv2
import cv2.aruco as aruco
from djitellopy import tello
import numpy as np
from Other import Other
import time

Start_time = time.time()

#루코마커의 중앙 값 결정
def getwhere(bbox):
    if len(bbox) == 0:
        return -1, -1
    a = np.reshape(bbox, (4, 2))
    return np.sum(a, axis=0)/4


#루코마커 탐지
def findaruco(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)         # 회색 이미지로 변환
    arucoDict = aruco.Dictionary_get(aruco.DICT_4X4_50)     # ArUco Dictionary 생성
    arucoParam = aruco.DetectorParameters_create()          # 오차 보정을 위한 파라미터 생성
    bboxs, ids, rejected = aruco.detectMarkers(imgGray,
                                               arucoDict, parameters=arucoParam)  # imgGray 에서 ArUco 마커 탐색
    print(bboxs)
    print(len(bboxs))
    return ids, bboxs

#목표 값 설정
goal = np.array([640, 360])

#그래프 그리기 및 PID 제어
calculation = Other(goal, np.array([0.1, 0.03, 0.02]))

#텔로 연결
drone = tello.Tello()
drone.connect()

#웹캠 연결 설정
cap = cv2.VideoCapture(0)       # 웹캠 연결
print("{}*{}\nfps : {}".format(cap.get(cv2.CAP_PROP_FRAME_HEIGHT), cap.get(cv2.CAP_PROP_FRAME_WIDTH),
                               cap.get(cv2.CAP_PROP_FPS)))

#실제 제어
drone.takeoff()
while True:
    ret, img = cap.read()   # 웹캠에서 사진 불러오기
    if not ret:
        continue
    cv2.imshow('test', img)   # 창에 사진 띄우기
    id, bbox = findaruco(img)   # 루코마커의 id와 4귀퉁이 찾기
    location = getwhere(bbox)
    velocity = calculation.do(location, time.time() - Start_time)   # 제어값 계산
    print(location, end='\n')
    print(velocity)
    drone.send_rc_control(-round(velocity[0]), 0, round(velocity[1]), 0)   # 제어 값 전송
    print("")
    if (cv2.waitKey(1) & 0xff) == ord('q'):
        break
drone.land()
cap.release()
calculation.draw()