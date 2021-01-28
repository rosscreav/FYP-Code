import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

frontleft = 17
frontright = 18
backright = 23

GPIO.setup(frontleft,GPIO.OUT)
GPIO.setup(frontright,GPIO.OUT)
GPIO.setup(backright,GPIO.OUT)

for i in range(10):
	time.sleep(1)
	GPIO.output(frontleft,True)
	time.sleep(1)
	GPIO.output(frontleft,False)
	
	time.sleep(1)
	GPIO.output(frontright,True)
	time.sleep(1)
	GPIO.output(frontright,False)
	
	time.sleep(1)
	GPIO.output(backright,True)
	time.sleep(1)
	GPIO.output(backright,False)	
	
