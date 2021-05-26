import cv2
from djitellopy import tello

daehwan = tello.Tello()
print(me.get_battery)
daehwan.send_rc_control(0, 0, 0, 0)

x_goal = 640
x_real = 000
x_factor = (x_goal - x_real)
xway = x_factor / abs(x_factor)

y_goal = 360
y_real = 000
y_factor = (y_goal - y_real)
yway = y_factor / abs(y_factor)

if abs(x_factor) / 100 >= 1:
    x_v = (20 + abs((x_factor) / 100) * 3) * xway
elif abs(x_factor) / 10 >= 1:
    x_v = (10 + abs(x_factor) / 10) * xway
else:
    x_v = (10 + abs(x_factor)) * xway

if abs(y_factor) / 100 >= 1:
    y_v = (20 + abs((y_factor) / 100) * 3) * yway
elif abs(x_factor) / 10 >= 1:
    y_v = (10 + abs(y_factor) / 10) * yway
else:
    y_v = (10 + abs(y_factor)) * yway