from djitellopy import tello
import time
drone = tello.Tello()
drone.takeoff()
time.sleep(5)
drone.land()
