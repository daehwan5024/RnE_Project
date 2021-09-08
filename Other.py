import numpy as np
import matplotlib.pyplot as plt

class Other:
    def __init__(self, goal, k_p, k_i, k_d, name):
        self.goal = goal
        self.location = []
        self.error = []
        self.time = []
        self.Integral = 0
        self.k_i = k_i
        self.k_p = k_p
        self.k_d = k_d
        self.length = 0
        self.name = str(name)

    def do(self, location, time):
        if location == -1 :
            return 0
        self.location.append(location)
        self.error.append(self.goal - location)
        self.time.append(time)
        self.length+=1
        if self.length == 1:
            derivative = 0

        else:
            derivative = (self.error[-1]-self.error[-2])/(self.time[-1] - self.time[-2])
            self.Integral += (self.error[-1] + self.error[-2]) * (self.time[-1] - self.time[-2]) / 2


        return (self.error[-1]*self.k_p + self.Integral*self.k_i + derivative*self.k_d)/3

    def draw(self):
        f = open(self.name+".txt", 'w')
        f.write(str(self.length) + "\n")
        f.write(str(self.time))
        f.write("\n\n\n\n\n\n")
        f.write(str(self.location_x) + "  " + str(self.location_y) + "\n\n")

        plt.plot(self.time, self.location_x, '.-')
        plt.savefig(self.name+'.png')
        plt.show()