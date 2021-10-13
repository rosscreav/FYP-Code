##Script for testing the ultrasound sensor
##Imports
import RPi.GPIO as GPIO
import time

##Cleanup all pins
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
##Setup pins for the Ultrasound sensor
TRIG = 21
ECHO = 20

##Setup the pins for IO 
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

##Set the trigger to false
GPIO.output(TRIG, False)
##Loop forever
while True:
	##Sleep between loops
	time.sleep(2)
	##Set trigger pin high
	GPIO.output(TRIG, True)
	##Wait a small amount of time
	time.sleep(0.00001)
	##Set trigger pin low
	GPIO.output(TRIG, False)


	##When pulse start record time
	while GPIO.input(echo)==0:
		pulse_start = time.time()
	##When pulse end record time
	while GPIO.input(echo)==1:
		pulse_end = time.time()

	##Length Calculation (cm)
	pulse_duration = pulse_end - pulse_start
	distance = pulse_duration * 17150
	distance = round(distance,2)
	##Print to console
	print(str(distance)+"cm")
