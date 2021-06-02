import numpy as np

class controll:

    def __init__(self, goal):
        self.goal = goal

    def get_speed(self, location):
        self.factor = self.goal - location
        self.way = self.factor/abs(self.factor)
        if abs(self.factor[0]) / 100 >= 1:
            x_v = (20 + abs((self.factor[0]) / 100) * 3) * self.way[0]
        elif abs(self.factor[0]) / 10 >= 1:
            x_v = (10 + abs(self.factor[0]) / 10) * self.way[0]
        else:
            x_v = (10 + abs(self.factor[0])) * self.way[0]

        if abs(self.factor[1]) / 100 >= 1:
            y_v = (20 + abs((self.factor[1]) / 100) * 3) * self.way[1]
        elif abs(self.factor[1]) / 10 >= 1:
            y_v = (10 + abs(self.factor[1]) / 10) * self.way[1]
        else:
            y_v = (10 + abs(self.factor[1])) * self.way[1]

        self.velocity = np.array([x_v, y_v])

        return self.velocity
