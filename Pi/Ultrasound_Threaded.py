##Imports
import RPi.GPIO as GPIO
import time
import threading

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
#TRIG = 21
#ECHO = 20

def read_ultrasound(trig,echo):
	if trig == 20:
	  print("right")
	GPIO.setup(trig,GPIO.OUT)
	GPIO.setup(echo,GPIO.IN)

	GPIO.output(trig, False)
	while True:
		time.sleep(2)
		GPIO.output(trig, True)
		time.sleep(0.00001)
		GPIO.output(trig, False)

		while GPIO.input(echo)==0:
		  pulse_start = time.time()


		while GPIO.input(echo)==1:
		  pulse_end = time.time()

		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration * 17150
		distance = round(distance,2)
		if trig == 20:
		  print("Right: "+str(distance))
		elif trig == 23:
		  print("Left: "+str(distance))

if __name__ == '__main__':
	thread = threading.Thread(target=read_ultrasound, args=(20,21), daemon=True)
	thread.start()
	thread2 = threading.Thread(target=read_ultrasound, args=(23,24), daemon=True)
	thread2.start()
	while True:
	  continue
