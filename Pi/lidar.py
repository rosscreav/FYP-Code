##Tests LIDAR sensors printing results to console
##Imports
import serial
import time

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

##Loop forver
while(True):
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