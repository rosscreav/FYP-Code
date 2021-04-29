##Imports
import RPi.GPIO as GPIO
import time
import threading
import serial
import motor_controller as mc

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
#TRIG = 21
#ECHO = 20
ultra_left = 0
ultra_right = 0
lidar = 0
left_update = False
right_update = False

ser = serial.Serial('/dev/ttyUSB0',115200,timeout = 1)
ser.write(0x42)
ser.write(0x57)
ser.write(0x02)
ser.write(0x00)
ser.write(0x00)
ser.write(0x00)
ser.write(0x01)
ser.write(0x06)


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
		  global ultra_right
		  ultra_right = distance	
		  right_update = True
		  #print("Right: "+str(distance))
		elif trig == 23:
		  global ultra_left
		  left_update = True
		  ultra_left = distance
		  #print("Left: "+str(distance))

#Read the date from the Lidar
def getTFminiData():
	while True:
		#print("waiting")
		while(ser.in_waiting >= 9):
			#Read and discard first two bytes
			ser.read()
			ser.read()
			#print("reading")
			#Read low and high disance bytes
			Dist_L = ser.read()
			Dist_H = ser.read()
			#Calculate the distance
			Dist_Total = (ord(Dist_H) * 256) + (ord(Dist_L))
			#Ignore other bytes
			for i in range (0,5):
					ser.read()
			#Print the distance
			#print(str(Dist_Total-3) + "cm")
			ser.flush()
			##Return the distance
			global lidar
			lidar = Dist_Total-3
			#return Dist_Total-3

if __name__ == '__main__':
	thread = threading.Thread(target=read_ultrasound, args=(20,21), daemon=True)
	thread.start()
	thread2 = threading.Thread(target=read_ultrasound, args=(23,24), daemon=True)
	thread2.start()
	thread3 = threading.Thread(target=getTFminiData, daemon=True)
	thread3.start()
	while True:
	if  lidar <5.5:
		mc.back()
		time.sleep(.2)
		mc.stop()
	if ((ultra_left < 5.5 and left_update) and (ultra_right < 5.5 and right_update)):
		#back
		mc.back()
		time.sleep(.2)
		mc.stop()
		left_update = False
		right_update = False
	elif ultra_right < 5.5 and right_update:
		mc.left()
		time.sleep(.20)
		mc.stop()
		right_update = False
	elif ultra_left < 5.5 and left_updatef:
		mc.right()
		time.sleep(.20)
		mc.stop()
		left_update = False