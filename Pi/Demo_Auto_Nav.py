##Robot automatically moves randomly around the room and avoids objects
##Imports
import RPi.GPIO as GPIO
import time
import threading
import serial
import motor_controller as mc
import random

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


##Method to turn the device away from an object in path
def turn_reset(direction):
	##Print to console
	print("turn reset started")
	##Wait for the left and right sensor to update their values
	while not right_update and not left_update:
		pass
	##If theres an object in front of the robot
	if direction == "front":
		##If theres more space on the left
		if ultra_left > ultra_right:
			##Print to console
			print("Lidar: Turning left")
			##Move left
			mc.left()
			##Sleep for a random length between 0.5 - 1.2s
			time.sleep(float(random.randint(5,12)/10.0))
			##stop turning
			mc.stop()
		##If theres more space on the right
		else:
			##Print to console
			print("Lidar: Turning right")
			##Move left
			mc.right()
			##Sleep for a random length between 0.5 - 1.2s
			time.sleep(float(random.randint(5,12)/10.0))
			##stop turning
			mc.stop()
	##If theres an object too close to the right side
	elif direction == "right":
		##Print to console
		print("Ultra: Turning left")
		##Turn left
		mc.left()
		##Sleep for .2s
		time.sleep(.20)
		##Stop turning 
		mc.stop()
	##If theres an object to close to the left side
	else:
		##Print to console
		print("Ultra: Turning right")
		##Turn right
		mc.right()
		##Sleep for .2s
		time.sleep(.20)
		##Stop turning right
		mc.stop()
	##After turning occurs restart forward movement
	mc.forward(speed=0.2)
	##Print to console
	print("turn rest ended")
	##Return
	return



##When called start sensor reading and start moving
if __name__ == '__main__':
	##Create a thread for each sensor and start them (updates global variables asynchronously)
	thread = threading.Thread(target=read_ultrasound, args=(20,21), daemon=True)
	thread.start()
	thread2 = threading.Thread(target=read_ultrasound, args=(23,24), daemon=True)
	thread2.start()
	thread3 = threading.Thread(target=getTFminiData, daemon=True)
	thread3.start()
	##Start moving forward
	mc.forward(speed=0.2)
	##Loop forver
	while True:
		##If distance in front < 5.5cm
		if  lidar <5.5:
			##Stop
			mc.stop()
			time.sleep(.01)
			##Start moving back
			mc.back()
			time.sleep(.2)
			##Stop moving back
			mc.stop()
			##Call turn reset with the direction as front
			turn_reset("front")
		##If the latest right reading < 5.5cm 
		if ultra_right < 5.5 and right_update:
			##Stop
			mc.stop()
			time.sleep(.01)
			##Start moving left
			mc.left()
			time.sleep(.20)
			##Stop moving left
			mc.stop()
			##Reset the latest reading flag
			right_update = False
			##Call turn reset with the direction as right
			turn_reset("right")
		##If the latest left reading < 5.5cm 
		elif ultra_left < 5.5 and left_update:
			##Stop
			mc.stop()
			time.sleep(.01)
			##Start moving right
			mc.right()
			time.sleep(.20)
			##Stop moving right
			mc.stop()
			##Reset the latest reading flag
			left_update = False
			##Call turn reset with the direction as left
			turn_reset("left")
