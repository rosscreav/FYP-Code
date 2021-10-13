##Robot detects when an object is too close and turns away
##Imports
import RPi.GPIO as GPIO
import time
import threading
import serial
import motor_controller as mc

##Clear any used pins from previous scripts
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

##Default values to send for intial data
ultra_left = 0
ultra_right = 0
lidar = 0
##Flags to say if the ultrasound has had an update in value
left_update = False
right_update = False

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

##Custom sensor reading method to update flags and manage both sensors
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

		##Ignore if a thread trys to write to variable while its being rad
		try:
			##Calculate the distance
			pulse_duration = pulse_end - pulse_start
			distance = pulse_duration * 17150
			distance = round(distance,2)
			##If trigger pin is the right sensor
			if trig == 20:
				##Update global variables
			  	global ultra_right
			  	global right_update
			  	##Update value and set flag to true
			  	ultra_right = distance	
			  	right_update = True
			##If trigger pin is the left sensor
			elif trig == 23:
				##Update global variables
			  	global ultra_left
			  	global left_update
			  	##Update value and set flag to true
			  	left_update = True
			  	ultra_left = distance
		##If variable is in use
		except:
			##Move to next loop and try again
			continue

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

##Main method
if __name__ == '__main__':
	##Create a thread for each sensor and start them (updates global variables asynchronously)
	thread = threading.Thread(target=read_ultrasound, args=(20,21), daemon=True)
	thread.start()
	thread2 = threading.Thread(target=read_ultrasound, args=(23,24), daemon=True)
	thread2.start()
	thread3 = threading.Thread(target=getTFminiData, daemon=True)
	thread3.start()
	while True:
		##Check if object < 5.5cm from lidar sensor
		if  lidar <5.5:
			##Move back for .2s
			mc.back()
			time.sleep(.2)
			##Stop
			mc.stop()
		##If theres an object <5.5cm to both sensors and the reading has been updated
		if ((ultra_left < 5.5 and left_update) and (ultra_right < 5.5 and right_update)):
			##Move back for .2s
			mc.back()
			time.sleep(.2)
			##Stop
			mc.stop()
			##Set the new data flags as false
			left_update = False
			right_update = False
		##If theres an object <5.5cm from the right ultrasound
		elif ultra_right < 5.5 and right_update:
			##Turn to the left for .2s
			mc.left()
			time.sleep(.20)
			##Stop
			mc.stop()
			##Set the new data flag as false
			right_update = False
		##If theres an object <5.5cm from the left ultrasound	
		elif ultra_left < 5.5 and left_update:
			##Turn to the right for .2s
			mc.right()
			time.sleep(.20)
			##Stop
			mc.stop()
			##Set the new data flag as false
			left_update = False
