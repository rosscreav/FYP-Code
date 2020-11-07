import socket
import urllib.request
import Get_IP
 
def decode_instruction(msg):
	if "FWD" in msg:
		print("moving forward")
	elif "BCK" in msg:
		print("moving back")
	elif "LEFT" in msg:
		print("moving left")
	elif "RIGHT" in msg:
		print("moving right")


localIP = Get_IP.get_ip()
print(localIP)

localPort   = 20001
bufferSize  = 1024

 

msgFromServer       = "Hello UDP Client"
bytesToSend         = str.encode(msgFromServer)
# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

# Listen for incoming datagrams
while(True):

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0]
    message = message.decode("utf-8")
    address = bytesAddressPair[1]

    clientMsg = "Message from Client: '{}' ".format(message)
    clientIP  = "Client IP Address:{}".format(address)

    decode_instruction(message.upper())
    
    print(clientMsg)
    print(clientIP)
    # Sending a reply to client

    UDPServerSocket.sendto(bytesToSend, address)
