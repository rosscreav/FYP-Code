##Imports
import RPi.GPIO as GPIO
import time

GPIO.cleanup()

TRIG1 = 23
ECHO2 = 24

GPIO.setmode(GPIO.BCM)

def read_ultrasound(trig, echo)
	GPIO.setup(trig,GPIO.OUT)
	GPIO.setup(echo,GPIO.IN)
	GPIO.output(trig, False)
	time.sleep(1)
	GPIO.output(TRIG, True)
	time.sleep(0.00001)
	GPIO.output(TRIG, False)
	##When pulse start
	while GPIO.input(ECHO)==0:
		pulse_start = time.time()
	##When pulse end
	while GPIO.input(ECHO)==1:
		pulse_end = time.time()

	##Length Calculation
	pulse_duration = pulse_end - pulse_start
	distance = pulse_duration * 17150
	distance = round(distance,2)
	return distance



