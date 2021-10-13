##A script to test motors when connected to GPIO pins (Poor functionaility do not use)
##Imports
import RPi.GPIO as GPIO
import time

##Set pinout
GPIO.setmode(GPIO.BCM)

##Motor connections
frontleft = 17
frontright = 18
backright = 23

##Set up pins for IO
GPIO.setup(frontleft,GPIO.OUT)
GPIO.setup(frontright,GPIO.OUT)
GPIO.setup(backright,GPIO.OUT)

##Loop 10 times
for i in range(10):
	##Turn front left motor on for 1 second
	time.sleep(1)
	GPIO.output(frontleft,True)
	time.sleep(1)
	GPIO.output(frontleft,False)
	
	##Turn front right motor on for 1 second
	time.sleep(1)
	GPIO.output(frontright,True)
	time.sleep(1)
	GPIO.output(frontright,False)
	
	##Turn back right motor on for 1 second
	time.sleep(1)
	GPIO.output(backright,True)
	time.sleep(1)
	GPIO.output(backright,False)	
	
