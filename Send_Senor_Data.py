import Read_Sensors
from firebase import firebase


fb = firebase.FirebaseApplication('https://fyp-database-7e287-default-rtdb.europe-west1.firebasedatabase.app/',None)

result = fb.post('/SensorData/',Read_Sensors.read_sensor_data())
print(result)
