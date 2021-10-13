##A script to recieve and process the UDP messages into commands
##Imports
import socket
import urllib.request
import Get_IP
 
##Method to decode instructions into commands returns string to client
def decode_instruction(msg):
	##Forward
	if "FWD" in msg:
		print("Moving forward")
		retval="Moved Forward"
	##Back 
	elif "BCK" in msg:
		print("Moving back")
		retval="Moved Back"
	##Left
	elif "LEFT" in msg:
		print("Moving left")
		retval="Moved Left"
	##Right
	elif "RIGHT" in msg:
		print("Moving right")
		retval="Moved Right"
	##Shut down server
	elif "SD" in msg:
		print("Sever shutdown")
		exit()
	##If unknown command sent
	else:
		print("Uknown command: {}".format(msg))
		retval="Uknown command: {}".format(msg)
	##Return string for client
	return retval

##Return the IP of the PI
localIP = Get_IP.get_ip()
##Print the IP to console
print(localIP)

##Pick a unused port a size for the server buffer
localPort   = 20001
bufferSize  = 1024

##Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
##Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
##Print to console
print("UDP server up and listening")

##Listen for incoming datagrams (Loop forever)
while(True):
	##Wait for a datagram
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    ##Extract and decode the message
    message = bytesAddressPair[0]
    message = message.decode("utf-8")
    ##Record the clients address
    address = bytesAddressPair[1]

    ##Print the message and address to console
    print("Message from Client: '{}' ".format(message))
    print("Client IP Address:{}".format(address))

    ##Decode the message from the client
    msgFromServer = decode_instruction(message.upper())
    ##Reply with the return value to the client
    bytesToSend  = str.encode(msgFromServer)

    ##Send reply to client
    UDPServerSocket.sendto(bytesToSend, address)
