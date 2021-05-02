##Imports
import RPi.GPIO as GPIO
import time
import threading
import serial
import motor_controller as mc
from mqtt import Publish as p
import random

ser = serial.Serial('/dev/ttyUSB0',115200,timeout = 1)
ser.write(0x42)
ser.write(0x57)
ser.write(0x02)
ser.write(0x00)
ser.write(0x00)
ser.write(0x00)
ser.write(0x01)
ser.write(0x06)

reading = False
lidar_measurements = []

#Read the date from the Lidar
def getTFminiData():
	while True and reading:
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

			lidar_measurements.append(Dist_Total-3)
			#return Dist_Total-3


if __name__ == '__main__':
	thread = threading.Thread(target=getTFminiData, daemon=True)
	thread.start()
	##Spin in circle
	mc.slow_turn()
	reading = True
	time.sleep(3.9)
	mc.stop()
	reading = False
	print("Measurement count: " len(lidar_measurements))
	print(lidar_measurements)
	##Read measurements 

	##Send map