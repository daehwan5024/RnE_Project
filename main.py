import cv2
import cv2.aruco as aruco
from djitellopy import tello
import numpy as np
from PID_Controll import controll
import time
from Graph_draw import Graph_drawer

'''루코마커의 중앙 값 결정'''
def getWhere(bbox): #루코마커의 중앙 위치 계산
    print(bbox)
    if(len(bbox)==0):
        return -1, -1
    a = np.reshape(bbox, (2, 4))
    return np.sum(a, axis=1)/4

'''루코마커 탐지'''
def findaruco(img, markerSize = 4, totalMarkers=50): #루코마커의 위치 반환
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #회색 이미지로 변환
    key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}') #필요한 ArUco 마커 Dictionary이름 생성
    arucoDict = aruco.Dictionary_get(key) #ArUco Dictionary 생성
    arucoParam = aruco.DetectorParameters_create() #오차 보정을 위한 파라미터 생성
    bboxs, ids, rejected = aruco.detectMarkers(imgGray, arucoDict, parameters=arucoParam) #imgGray에서 ArUco 마커 탐색
    return ids, bboxs

'''목표 값 설정'''
goal = np.array([640, 360])

'''그래프 그리는 클래스'''
draw = Graph_drawer(goal)

'''텔로 연결'''
drone = tello.Tello() #텔로 드론 조종을 위한 변수 설정
drone.connect() #텔로 드론과 연결
print(drone.get_battery()) #배터리 상태를 받는다
drone.send_rc_control(0, 0, 0, 0) #드론을 (좌우 속도, 앞뒤 속도, 위 아래 속도, yaw 회전 속도)로 지정한다

'''웹캠 연결 설정'''
cap = cv2.VideoCapture(0) #웹캠 연결
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) #사진 가로 픽셀 수
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720) #사진 세로 픽셀 수
cap.set(cv2.CAP_PROP_FPS, 30.0) #프레임수 결정

'''PID 제어 클래스 만들기'''
controller = controll(goal, np.array([0.1, 0.03, 0.02]), 1/cap.get(cv2.CAP_PROP_FPS)) #PID제어를 위한 Class 정의

'''실제 제어'''
while True:
    ret, img = cap.read() #웹캠에서 사진 불러오기
    if not ret:
        continue
    cv2.imshow('test', img) #창에 사진 띄우기
    id, bbox = findaruco(img) #루코마커의 id와 4귀퉁이 찾기
    location = getWhere(bbox)
    draw.append(location)
    velocity = controller.get_speed(location) #제어값 계산
    print(velocity)
    drone.send_rc_control(int(velocity[0]), 0, int(velocity[1]), 0) #제어 값 전송
    draw.draw()

    if (cv2.waitKey(1) & 0xff) == ord('q'):
        break
draw.draw()
cap.release()
