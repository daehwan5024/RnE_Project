import numpy as np

class controll:
    def __init__(self, goal, K_PID, dt):
        self.goal = goal
        self.K = K_PID
        self.dt = dt
        self.previous = np.array([0,0])
        self.Integral = np.array([0,0])
        print(self.dt)

    def get_speed(self, location):
        self.factor = (self.goal - location)
        self.Integral = self.Integral+self.factor*self.dt
        self.velocity = self.factor*self.K[0] + self.Integral*self.K[1] + ((self.factor - self.previous)/self.dt)*self.K[2]
        self.previous = self.factor

        return self.velocity
