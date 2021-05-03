
from firebase import firebase

def send(data,directory):
	fb = firebase.FirebaseApplication('https://fyp-database-7e287-default-rtdb.europe-west1.firebasedatabase.app/',None)
	result = fb.post('/'+directory+'/',data)
	print(result)
