from adafruit_motorkit import MotorKit
import time

k = MotorKit()

k.motor1.throttle = -0.5
k.motor2.throttle = -0.5
k.motor3.throttle = 0.5
k.motor4.throttle = 0.5

time.sleep(4)

k.motor1.throttle = 0
k.motor2.throttle = 0
k.motor3.throttle = 0
k.motor4.throttle = 0
