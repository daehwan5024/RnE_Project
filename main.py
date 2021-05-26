import cv2
import cv2.aruco as aruco
from djitellopy import tello
from time import sleep
import numpy as np

goal_x = 640
goal_y = 360

def findaruco(img, markerSize = 6, totalMarkers=50, draw=True):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
    arucoDict = aruco.Dictionary_get(aruco.DICT_4X4_50)
    arucoParam = aruco.DetectorParameters_create()
    bboxs, ids, rejected = aruco.detectMarkers(imgGray, arucoDict, parameters=arucoParam)
    return ids, bboxs

def getWhere(bbox):
    print(type(bbox))
    print(bbox)
    if(len(bbox)==0):
        return -1, -1


def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_XI_FRAMERATE, 60.0)
    while(True):
        ret, img = cap.read()
        cv2.imshow('test', img)
        id, bbox = findaruco(img)
        x, y = getWhere(bbox)
        print(x)
        print(y)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break



if __name__ == "__main__":
    main()
