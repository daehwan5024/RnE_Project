import numpy as np
from matplotlib import pyplot as plt
import time

class controll:
    def __init__(self, goal, K_PID, dt):
        self.goal = goal    # 목표 위치
        self.K = K_PID      # PID 제어를 위한 비례상수 1*3크기이며 순서대로 K_p, K_i, K_d이다
        self.dt = dt        # 시간 간격으로 1/카메라의 프레임수 이다.
        self.previous = np.array([0, 0])  # 바로 전의 값을 저장한다.
        self.Integral = np.array([0, 0])  # 현재 까지의 적분값을 저장한다.
        print(self.dt)

    def get_speed(self, location):
        if(location[0] == -1 and location[1]==-1):
            return np.array([0, 0])
        self.factor = (self.goal - location)    # 오차 계산
        self.velocity = self.factor*self.K[0] + self.Integral*self.K[1] + ((self.factor - self.previous)/self.dt)*self.K[2] #PID제어를 위한 값 계산
        self.Integral = self.Integral+self.factor*self.dt    # 적분 값 계산
        self.previous = self.factor     # 바로 전의 값을 현재 값으로 업데이트

        return self.velocity/3  # 계산한 값 리턴
