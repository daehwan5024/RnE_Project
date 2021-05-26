from djitellopy import tello

daehwan = tello.Tello()
print(me.get_battery)

x_goal = 640
x_real = 000
x_factor = (x_goal - x_real)

if x_factor >= 0:

if abs(x_factor) / 100 > 8:
    daehwan.send_rc_control(30, )
