##Upload 20 mock data JSON to the database using random values
##Used for testing the Real time plotting on the server side
##Imports
import time
from firebase import firebase
from numpy import random as numpy

##Connect to the firebase 
fb = firebase.FirebaseApplication('https://fyp-database-7e287-default-rtdb.europe-west1.firebasedatabase.app/',None)

##Mean value of data being 16 with deviation of 16
mean = 60
deviation = 16

##Loop 20
for x in range(20):
        ##Upload a mock piece of data to the MockedData directory
        result = fb.post('/MockedData/', {"ultra_left":numpy.normal(mean,deviation),"ultra_right":numpy.normal(mean,deviation),"lidar":numpy.normal(mean,deviation),"timestamp":time.time()})
        ##Wait 5 seconds
        time.sleep(5)


