##A script to help the Pi identify a corner (poor performance) -- UNUSED
##Imports
import Read_Sensors as sensor
import motor_controller as motor

##Prints corner identified as it passes a corner
def identify_corner():
        ##Start slowly turning in a circle
        motor.slow_turn()
        ##Creates a buffer array for the LIDAR values 
        values = []
        print("Starting")
        while True:
                print("Current Values:")
                print(values)
                ##Reads LIDAR sensor and places it into the array
                values.append(sensor.getTFminiData())
                ##If there is 6 values in the buffer
                if len(values) > 5:
                        ##if the average first two values < middle value(cornerpoint) > average of last two values
                        ##so if values were small got big and got small again using averages for accuracy 
                        if (values[0] / 2 + values[1] / 2) < values[3] > (values[4] / 2 + values[5] / 2):
                                ##Print to console
                                print("Corner Identified")
                                ##break loop for debugging
                                break
                        ##Pop a value in the array to maintain size
                        values.pop(0)
        print("Function continuing")


##If called for testing
if __name__ == '__main__':
        identify_corner()

