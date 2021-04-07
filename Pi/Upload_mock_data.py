import Read_Sensors
import time
from firebase import firebase
from numpy import random as numpy

fb = firebase.FirebaseApplication('https://fyp-database-7e287-default-rtdb.europe-west1.firebasedatabase.app/',None)

mean = 60
deviation = 16

for x in range(20):
        result = fb.post('/MockedData/', {"ultra_left":numpy.normal(mean,deviation),"ultra_right":numpy.normal(mean,deviation),"lidar":numpy.normal(mean,deviation),"timestamp":time.time()})
        time.sleep(5)


