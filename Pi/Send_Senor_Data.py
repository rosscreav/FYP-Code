##Script to read the sensor data and send it to firebase
##Imports
import Read_Sensors
from firebase import firebase

##Create the firebase connection
fb = firebase.FirebaseApplication('https://fyp-database-7e287-default-rtdb.europe-west1.firebasedatabase.app/',None)
##Post the data to the database under SensorData
result = fb.post('/SensorData/',Read_Sensors.read_sensor_data())
##Print the confirmation
print(result)
