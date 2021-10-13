##A script to read both ultrasounds and LIDAR sensors (importable) 
##Imports
import RPi.GPIO as GPIO
import time
import serial

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

#Pinout for the left ultrasound 
trig_l = 21
echo_l = 20
#Pinout for the right ultrasound 
trig_r = 24
echo_r = 23

#Set pinout the BCM numbering format
GPIO.setmode(GPIO.BCM)

#Read the ultrasound on the inputted pins
def read_ultrasound(trig, echo):
	#Setup pins
	GPIO.setup(trig,GPIO.OUT)
	GPIO.setup(echo,GPIO.IN)
	#Set trig to 0
	GPIO.output(trig, False)
	#Wait for the pin to settle at low
	time.sleep(1)
	#Set the trigger pin high
	GPIO.output(trig, True)
	#Turn off pin after 0.00001s
	time.sleep(0.00001)
	GPIO.output(trig, False)
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
	##Return distance in centimeters rounded to 2 decimals
	return distance

##Read the data from the Lidar
def getTFminiData():
	##Wait till full 9 bits are queued 
    while(ser.in_waiting >= 9):
    	##Read and discard first two bytes (error check bits #TODO handle error)
        ser.read()
        ser.read()
  		
  		##Read low and high disance bytes
        Dist_L = ser.read()
        Dist_H = ser.read()
        ##Calculate the distance
        Dist_Total = (ord(Dist_H) * 256) + (ord(Dist_L))
        ##Ignore other bytes
        for i in range (0,5):
            ser.read()
        ##Print the distance to console
        print(str(Dist_Total-3) + "cm")
        #Flush the serial port
        ser.flush()
        ##Return the distance
        return Dist_Total-3

##Method to return the data as a json from each sensor
def read_sensor_data():
	#Read both ultrasound
	ultrasound_l = read_ultrasound(trig_l,echo_l)
	ultrasound_r = read_ultrasound(trig_r,echo_r)
	#Read LIDAR
	lidar = getTFminiData()
	#Cleanup pinouts
	GPIO.cleanup()
	#Print readings
	print(ultrasound_l)
	print(ultrasound_r)
	#Return data in format for firebase including timestamp
	return {"ultra_left" : ultrasound_l,"ultra_right" : ultrasound_r, "lidar" : lidar, "timestamp" : time.time()}

#if called for a test just read sensors once
if __name__ == "main":
	read_sensor_data()
