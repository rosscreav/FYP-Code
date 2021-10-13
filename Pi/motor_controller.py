##Importable scripts to manage the control of the motors
##Imports
from adafruit_motorkit import MotorKit
import time

##Intialise the motorkit on import or call
k = MotorKit()

##Motors are identical so to go straight and on oppisite sites they must go in oppisite directions

#Move forward (d specfies the direction 1 is forward -1 is back)
def forward(d=1,speed=0.25):
	k.motor1.throttle = speed*d
	k.motor2.throttle = -speed*d

##Move backwards
def back():
	##Calls forward with the direction as -1
	forward(-1)

##Turn to the right spins motors in opisite directions with optional input for direction
def left(d=1):
	k.motor1.throttle = -0.25*d
	k.motor2.throttle = -0.25*d
	
##Turn to the right (calls left with direction of -1)
def right():
	left(-1)

##Slowly rotate in towards the left (used for mapping)
def slow_turn():
	k.motor1.throttle = -0.18
	k.motor2.throttle = -0.18

##Stop the motors from turning
def stop():
	k.motor1.throttle = 0
	k.motor2.throttle = 0

##Simple test if file is called 
##(forward 1s--right 2s--slow turn left for 5s-- stop)
if __name__ == "__main__":
	forward()
	time.sleep(1)
	right()
	time.sleep(2)
	stop()
	slow_turn()
	time.sleep(5)
	stop()
