##Importable script to send data to firebase
##Imports
from firebase import firebase

##Send data to the database under a given directory in the database
def send(data,directory):
	##Create the connection
	fb = firebase.FirebaseApplication('https://fyp-database-7e287-default-rtdb.europe-west1.firebasedatabase.app/',None)
	##Post the data to the directory 
	result = fb.post('/'+directory+'/',data)
	##Print the transaction acknowlegment 
	print(result)
