
import socket


serverAddressPort   = ("raspberrypi", 20001)

bufferSize          = 1024

 

# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

 
while True:
	msgFromClient=input("Enter Message to send:")

	bytesToSend         = str.encode(msgFromClient)
	# Send to server using created UDP socket
	UDPClientSocket.sendto(bytesToSend, serverAddressPort)

	if msgFromClient.upper()=="SD":
		print("UDP Shutdown intialised")
		exit()

	msgFromServer = UDPClientSocket.recvfrom(bufferSize)

	 

	msg = "Message from Server {}".format(msgFromServer[0])

	print(msg)