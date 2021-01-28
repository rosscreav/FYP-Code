import motor_controller
import time

def decode_instruction(msg):
	if "FWD" in msg:
		print("Moving forward")
		motor_controller.forward()
		time.sleep(1)
		motor_controller.stop()
		retval="Moved Forward"
	elif "BCK" in msg:
		print("Moving back")
		motor_controller.back()
		time.sleep(1)
		motor_controller.stop()
		retval="Moved Back"
	elif "LEFT" in msg:
		print("Moving left")
		motor_controller.left()
		time.sleep(1)
		motor_controller.stop()
		retval="Moved Left"
	elif "RIGHT" in msg:
		print("Moving right")
		motor_controller.right()
		time.sleep(1)
		motor_controller.stop()
		retval="Moved Right"
	elif "SD" in msg:
		print("Sever shutdown")
		exit()
	else:
		print("Uknown command: {}".format(msg))
		retval="Uknown command: {}".format(msg)
	return retval


localIP = Get_IP.get_ip()
print(localIP)

localPort   = 20001
bufferSize  = 1024

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

    print("Message from Client: '{}' ".format(message))
    print("Client IP Address:{}".format(address))

    msgFromServer = decode_instruction(message.upper())
    bytesToSend         = str.encode(msgFromServer)

    # Sending a reply to client

    UDPServerSocket.sendto(bytesToSend, address)
