from adafruit_motorkit import MotorKit
import time

#Intialise the motorkit
k = MotorKit()

#Go forward
def forward(d=1):
	k.motor1.throttle = 0.25*d
	k.motor2.throttle = -0.25*d

#Go back
def back():
	forward(-1)

#Turn right
def left(d=1):
	k.motor1.throttle = -0.25*d
	k.motor2.throttle = -0.25*d
	
#Trun left
def right():
	left(-1)

#Slow rotate
def slow_turn():
	k.motor1.throttle = -0.1
	k.motor2.throttle = -0.1

#Turn off motors
def stop():
	k.motor1.throttle = 0
	k.motor2.throttle = 0

##Simple test if file is called
if __name__ == "__main__":
	forward()
	time.sleep(1)
	right()
	time.sleep(2)
	stop()
