import cv2 as cv
import numpy as np
from djitellopy import tello
from Other import Other
import time

hsv = 95
lower_blue1 = np.array([95, 95, 95])
upper_blue1 = np.array([105, 255, 255])
lower_blue2 = np.array([85, 95, 95])
upper_blue2 = np.array([95, 255, 255])
lower_blue3 = np.array([85, 95, 95])
upper_blue3 = np.array([95, 255, 255])

cv.namedWindow('img_color')

cv.namedWindow('img_result')


def GetMiddle(img_color):

    # 원본 영상을 HSV 영상으로 변환
    img_hsv = cv.cvtColor(img_color, cv.COLOR_BGR2HSV)
    img_mask1 = cv.inRange(img_hsv, lower_blue1, upper_blue1)
    img_mask2 = cv.inRange(img_hsv, lower_blue2, upper_blue2)
    img_mask3 = cv.inRange(img_hsv, lower_blue3, upper_blue3)
    img_mask = img_mask1 | img_mask2 | img_mask3

    kernel = np.ones((11, 11), np.uint8)
    img_mask = cv.morphologyEx(img_mask, cv.MORPH_OPEN, kernel)
    img_mask = cv.morphologyEx(img_mask, cv.MORPH_CLOSE, kernel)

    # 마스크 이미지로 원본 이미지에서 범위값에 해당되는 영상 부분을 획득
    img_result = cv.bitwise_and(img_color, img_color, mask=img_mask)

    numOfLabels, img_label, stats, centroids = cv.connectedComponentsWithStats(img_mask)
    returnX = -1
    returnY = -1

    for idx, centroid in enumerate(centroids):
        if stats[idx][0] == 0 and stats[idx][1] == 0:
            continue

        if np.any(np.isnan(centroid)):
            continue

        x, y, width, height, area = stats[idx]
        centerX, centerY = int(centroid[0]), int(centroid[1])
        print(centerX, centerY)

        if area > 900:
            returnX = centerX
            returnY = centerY
            cv.circle(img_color, (centerX, centerY), 10, (0, 0, 255), 10)
            cv.rectangle(img_color, (x, y), (x + width, y + height), (0, 0, 255))

    cv.imshow('img_color', img_color)
    cv.imshow('img_mask', img_mask)
    cv.imshow('img_result', img_result)
    return returnX, returnY

cap = cv.VideoCapture(0)
print("{}*{}\nfps : {}".format(cap.get(cv.CAP_PROP_FRAME_HEIGHT), cap.get(cv.CAP_PROP_FRAME_WIDTH),
                               cap.get(cv.CAP_PROP_FPS)))

pid_x = Other(320, 0.25, 0.0, 0.0, "X")
pid_y = Other(240, 0.25, 0.0, 0.0, "Y")

drone = tello.Tello()
drone.connect()
drone.takeoff()

Start_time = time.time()

while True:
    ret, img = cap.read()
    if not ret :
        continue
    x, y = GetMiddle(img)
    velocity_x, velocity_y = pid_x.do(x, time.time() - Start_time), pid_y.do(y, time.time() - Start_time)  # 제어값 계산
    print(str(velocity_x)+" "+str(velocity_y))
    drone.send_rc_control(-int(velocity_x), 0, int(velocity_y), 0)  # 제어 값 전송

    print("")
    if (cv.waitKey(1) & 0xff) == 27:
        break
drone.land()
cap.release()
cv.destroyAllWindows()
