##A simple script to return the the IP of the PI
##Imports
import socket

##Gets the IP
def get_ip():
	##Create a new socket
	s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	try:
		##Create a connection to the Bogon address
		s.connect(('10.255.255.255',1))
		##Get the socket name which represents your IP
		IP=s.getsockname()[0]
	except Exception:
		##If something goes wrong default
		print('Defaulting to local host')
		IP='127.0.0.1'
	finally:
		##close the socket
		s.close
	##Return the IP
	return IP

##Print out the current IP
if __name__ == '__main__':
	print(get_ip())
