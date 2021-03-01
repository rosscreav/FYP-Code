import serial
import time

ser = serial.Serial('/dev/ttyUSB0',115200,timeout = 1)
ser.write(0x42)
ser.write(0x57)
ser.write(0x02)
ser.write(0x00)
ser.write(0x00)
ser.write(0x00)
ser.write(0x01)
ser.write(0x06)

while(True):
    
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
