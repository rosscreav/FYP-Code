##Imports
import RPi.GPIO as GPIO
import time
import threading

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
#TRIG = 21
#ECHO = 20

def read_ultrasound(trig,echo):
	GPIO.setup(trig,GPIO.OUT)
	GPIO.setup(echo,GPIO.IN)

	GPIO.output(TRIG, False)
	while True:
		time.sleep(2)
		GPIO.output(TRIG, True)
		time.sleep(0.00001)
		GPIO.output(TRIG, False)

		while GPIO.input(ECHO)==0:
		  pulse_start = time.time()

		while GPIO.input(ECHO)==1:
		  pulse_end = time.time()

		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration * 17150
		distance = round(distance,2)

if __name__ == '__main__':
	thread = threading.Thread(target=read_ultrasound, args=(21,20))
	thread2 = threading.Thread(target=read_ultrasound, args=(23,24))