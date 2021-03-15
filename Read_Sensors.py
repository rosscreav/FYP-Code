##Imports
import RPi.GPIO as GPIO
import time
import serial

ser = serial.Serial('/dev/ttyUSB0',115200,timeout = 1)
ser.write(0x42)
ser.write(0x57)
ser.write(0x02)
ser.write(0x00)
ser.write(0x00)
ser.write(0x00)
ser.write(0x01)
ser.write(0x06)

trig_l = 21
echo_l = 20

trig_r = 24
echo_r = 23

GPIO.setmode(GPIO.BCM)

def read_ultrasound(trig, echo):
	GPIO.setup(trig,GPIO.OUT)
	GPIO.setup(echo,GPIO.IN)
	GPIO.output(trig, False)
	time.sleep(1)
	GPIO.output(trig, True)
	time.sleep(0.00001)
	GPIO.output(trig, False)
	##When pulse start
	while GPIO.input(echo)==0:
		pulse_start = time.time()
	##When pulse end
	while GPIO.input(echo)==1:
		pulse_end = time.time()

	##Length Calculation
	pulse_duration = pulse_end - pulse_start
	distance = pulse_duration * 17150
	distance = round(distance,2)
	return distance

def getTFminiData():
    while(ser.in_waiting >= 9):
        ser.read()
        ser.read()
   

        Dist_L = ser.read()
        Dist_H = ser.read()
        Dist_Total = (ord(Dist_H) * 256) + (ord(Dist_L))
        for i in range (0,5):
            ser.read()
        print(str(Dist_Total-3) + "cm")
        ser.flush()
        return Dist_Total-3

def read_sensor_data():
	ultrasound_l = read_ultrasound(trig_l,echo_l)
	ultrasound_r = read_ultrasound(trig_r,echo_r)
	#lidar = getTFminiData()
	#f = open("image.png", "r")
	GPIO.cleanup()
	print(ultrasound_l)
	print(ultrasound_r)
	#return {"ultra_left" : 20.23, "ultra_right" : 20.2, "lidar" : 20.32, "timestamp" : time.time()}
	#return {"ultra_left" : ultrasound_l,"ultra_right" : ultrasound_r, "lidar" : lidar}

read_sensor_data()
