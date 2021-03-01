from adafruit_motorkit import MotorKit
import time

k = MotorKit()

def forward(d=1):
	k.motor1.throttle = 0.25*d
	k.motor2.throttle = -0.25*d

def back():
	forward(-1)

def right(d=1):
	k.motor1.throttle = -0.25*d
	k.motor2.throttle = -0.25*d
	time.sleep(1)
	

def left():
	right(-1)

def stop():
	k.motor1.throttle = 0
	k.motor2.throttle = 0

if __name__ == "__main__":
	forward()
	time.sleep(1)
	right()
	time.sleep(0.2)
	stop()
