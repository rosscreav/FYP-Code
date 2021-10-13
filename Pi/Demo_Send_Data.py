##A script to send live sensor data over MQTT (used with mqtt/Read_Dict)
##Imports
import RPi.GPIO as GPIO
import time
import threading
import serial
from mqtt import Publish as p
import firebase_send as fire

##Clear any used pins from previous scripts
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

##Default values to send for intial data
ultra_left = 0
ultra_right = 0
lidar = 0

#Write the command to the serial bus to activate Lidar sensor
ser = serial.Serial('/dev/ttyUSB0',115200,timeout = 1)
ser.write(0x42)
ser.write(0x57)
ser.write(0x02)
ser.write(0x00)
ser.write(0x00)
ser.write(0x00)
ser.write(0x01)
ser.write(0x06)


#Read the ultrasound on the inputted pins (Loops forever and writes to globals and console)
def read_ultrasound(trig,echo):
	GPIO.setup(trig,GPIO.OUT)
	GPIO.setup(echo,GPIO.IN)
	##Set trigger to 0 before starting 
	GPIO.output(trig, False)
	##Loop forever
	while True:
		##Send out the trigger pulse
		GPIO.output(trig, True)
		time.sleep(0.00001)
		GPIO.output(trig, False)

		##While the pin is at 0 wait and record time
		while GPIO.input(echo)==0:
		  pulse_start = time.time()

		##Wait till the pin stops being high and record the time
		while GPIO.input(echo)==1:
		  pulse_end = time.time()

		##Length Calculation (cm)
		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration * 17150
		distance = round(distance,2)

		##If trigger pin is the right sensor
		if trig == 20:
		  ##Write to the global variable and print to console
		  global ultra_right
		  ultra_right = distance	
		##If trigger pin is the left sensor
		elif trig == 23:
		  ##Write to the global variable and print to console
		  global ultra_left
		  ultra_left = distance


##Read the date from the Lidar sensor
def getTFminiData():
	##Loop forver
	while True:
		##Wait till full 9 bits are queued 
		while(ser.in_waiting >= 9):
			##Read and discard first two bytes
			ser.read()
			ser.read()

			##Read low and high disance bytes
			Dist_L = ser.read()
			Dist_H = ser.read()
			##Calculate the distance
			Dist_Total = (ord(Dist_H) * 256) + (ord(Dist_L))
			##Ignore remaining bytes distance is all thats wanted
			for i in range (0,5):
					ser.read()
			##Flush the serial port
			ser.flush()
			##Update the global variable
			global lidar
			lidar = Dist_Total-3

##Main method prints dictionary and publishes to MQTT
if __name__ == '__main__':
	##Create a thread for each ultransound and for the LIDAR
	thread = threading.Thread(target=read_ultrasound, args=(20,21), daemon=True)
	thread.start()
	thread2 = threading.Thread(target=read_ultrasound, args=(23,24), daemon=True)
	thread2.start()
	thread3 = threading.Thread(target=getTFminiData, daemon=True)
	thread3.start()
	##Loop forever sending the data every second
	while True:
	  ##Create the dictionary
	  dict = {"ultra_left" : ultra_left,"ultra_right" : ultra_right, "lidar" : lidar, "timestamp" : time.time()}
	  ##Send data to firebase
	  fire.send(dict,'RealData')
	  ##Send to MQTT broker
	  p.send(dict,location='Pi')
	  ##Print to console
	  print(dict)
	  ##Wait for new sensor values (asynchronous updates)
	  time.sleep(1)
