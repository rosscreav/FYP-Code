from adafruit_motorkit import MotorKit
import time

k = MotorKit()

def forward(d=1):
	k.motor1.throttle = -0.5*d
	k.motor2.throttle = -0.5*d
	k.motor3.throttle = 0.5*d
	k.motor4.throttle = 0.5*d

def back():
	forward(-1)

def right(d=1):
	k.motor1.throttle = -0.5*d
	k.motor2.throttle = 0.5*d
	k.motor3.throttle = -0.5*d
	k.motor4.throttle = 0.5*d
	time.sleep(1)
	

def left():
	right(-1)

def stop():
	k.motor1.throttle = 0
	k.motor2.throttle = 0
	k.motor3.throttle = 0
	k.motor4.throttle = 0

if __name__ == "__main__":
	forward()
	sleep(5)
	back()
	sleep(5)
	right()
	sleep(5)
	left()
	sleep(5)
