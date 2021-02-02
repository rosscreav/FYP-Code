##Imports
import RPi.GPIO as GPIO
import time
import serial

ser = serial.Serial("/dev/ttyAMA0", 115200)

trig_l = 23
echo_l = 24

trig_r = 23
echo_r = 24

GPIO.setmode(GPIO.BCM)

def read_ultrasound(trig, echo)
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
    while True:
        count = ser.in_waiting
        if count > 8:
            recv = ser.read(9)
            ser.reset_input_buffer()
            if recv[0] == 'Y' and recv[1] == 'Y': # 0x59 is 'Y'
                low = int(recv[2].encode('hex'), 16)
                high = int(recv[3].encode('hex'), 16)
                distance = low + high * 256
                return distance

def read_sensor_data():
	ultrasound_l = read_ultrasound(trig_l,echo_l)
	ultrasound_r = read_ultrasound(trig_r,echo_r)
	lidar = getTFminiData()
	GPIO.cleanup()
	return {"left" : ultrasound_l,"right" : ultrasound_r, "front" : lidar}

