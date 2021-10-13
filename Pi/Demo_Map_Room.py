##Script to collect the data for the room map and send it to firebase
##Imports
import RPi.GPIO as GPIO
import time
import threading
import serial
import motor_controller as mc
from mqtt import Publish as p
import random
from firebase import firebase

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

##Currently reading flag
reading = False
##Array to hold the LIDAR measurements
lidar_measurements = []

##Read the data from the Lidar
def getTFminiData():
	##Loop forever
	while True:
		##Wait till full 9 bits are queued and reading is occuring
		while(ser.in_waiting >= 9 and reading):
			##Read and discard first two bytes
			ser.read()
			ser.read()
			
			##Read low and high disance bytes
			Dist_L = ser.read()
			Dist_H = ser.read()
			#Calculate the distance
			Dist_Total = (ord(Dist_H) * 256) + (ord(Dist_L))
			#Ignore other bytes
			for i in range (0,5):
					ser.read()
			##Flush the serial port
			ser.flush()
			##Call the global array
			global lidar_measurements
			##Append the current measurement to the list
			lidar_measurements.append(Dist_Total-3)

##Main function to aquire and send data
def map():
	##Create a thread to keep reading data and record when reading flag is on
	thread = threading.Thread(target=getTFminiData, daemon=True)
	thread.start()
	##Call global flag
	global reading
	##Turn slowly to the left
	mc.slow_turn()
	##Read the LIDAR while reading is high
	reading = True
	##Wait for full rotation (Gryoscope needed for accuracy) (1 rotation approx 4.35s)
	time.sleep(4.35)
	##Stop rotating
	mc.stop()
	##Stop reading lidar values
	reading = False
	##Count the number of measurements taken (can vary with serial input and background processes)
	print("Measurement count: " +str(len(lidar_measurements)))
	##Print the measurements to console
	print(lidar_measurements)
	##Create a dictionary to send the  data to firebase in JSON format
	d = dict(enumerate(lidar_measurements))
	##Connect to firebase
	fb = firebase.FirebaseApplication('https://fyp-database-7e287-default-rtdb.europe-west1.firebasedatabase.app/',None)
	##Post the data to the Map data directory
	result = fb.post('/MapData/',d)
	##print the confirmation
	print(result)

##If name = main call map()
if __name__ == '__main__':
	map()