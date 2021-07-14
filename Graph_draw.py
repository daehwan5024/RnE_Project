import numpy as np
from matplotlib import pyplot as plt
import time

class Graph_drawer:
    def __init__(self, goal):
        print("Graph drawer ready")
        self.x = np.array([])
        self.y = np.array([])
        self.t = np.array([])
        self.goal = goal
        self.start_time = time.time()

    def append(self, location):
        if(location[0]==-1 and location[1]==-1):
            return

        self.x = np.append(self.x, location[0])
        self.y = np.append(self.y, location[1])
        self.t = np.append(self.t, time.time()-self.start_time)

    def draw(self):
        plt.subplot(2, 1, 1)
        plt.plot(self.t, self.x, '.-')
        plt.subplot(2, 1, 2)
        plt.plot(self.t, self.y, '.-')
        plt.show()