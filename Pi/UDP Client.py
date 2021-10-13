##UDP script to send datagrams to the Pi from console input
##Imports
import socket

##Server information for the Pi (hostname,port number, buffer size)
serverAddressPort   = ("raspberrypi", 20001)
bufferSize          = 1024

##Create a UDP socket on the client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

##Loop forever
while True:
	##Look for input from the console
	msgFromClient=input("Enter Message to send:")

	##Encode the string into byte format
	bytesToSend = str.encode(msgFromClient)
	##Send to server using the UDP socket
	UDPClientSocket.sendto(bytesToSend, serverAddressPort)

	##If the client is sending Shutdown
	if msgFromClient.upper()=="SD":
		##Exit this script
		print("UDP Shutdown intialised")
		exit()

	##Get the return message from the server
	msgFromServer = UDPClientSocket.recvfrom(bufferSize)
	##Get the message from the server and format it as a string
	msg = "Message from Server {}".format(msgFromServer[0])
	##Print the formatted message to console
	print(msg)