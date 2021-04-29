import paho.mqtt.client as paho
import numpy as np
import json
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading

lidar_readings = []
ultra_right_readings = []
ultra_left_readings =[]

# Create figure for plotting
fig, ax = plt.subplots(nrows=3, ncols=1)
fig.tight_layout()
xs = []
ys = []



##Print out when subscribed succesfully
def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

##What to do for each message
def on_message(client, userdata, msg):
	global lidar_readings
	global ultra_right_readings
	global ultra_left_readings

	if "lidar" not in str(msg.payload):
		print("passing")
		return 
	#Print the message details
	#print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
	#print(str(msg.payload))
	string = msg.payload.decode('UTF-8').replace("'",'"')
	print(string)
	dict_val = json.loads(string)

	print("lidar " + str(dict_val["lidar"]))
	lidar_readings.append(float(dict_val["lidar"]))
	lidar_readings.pop(0)

	print("ultra_right " + str(dict_val["ultra_right"]))
	ultra_right_readings.append(float(dict_val["ultra_right"]))
	ultra_right_readings.pop(0)

	print("ultra_left " + str(dict_val["ultra_left"]))
	ultra_left_readings.append(float(dict_val["ultra_left"]))
	ultra_left_readings.pop(0)

	print("timestamp " + str(dict_val["timestamp"]))
	print("\n")

    
    


#Keep looping for messages and execute on_message on recieving a messgae
def sub_loop():
    client = paho.Client()
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    ##My Mqtt server
    client.connect('broker.mqttdashboard.com', 1883)
    client.subscribe('FYP_Mqtt_Messaging/Pi', qos=1)

    client.loop_forever()

def plotting():
	while True:

		global lidar_readings
		#ys = lidar_readings
		print("plotting: "+str(lidar_readings))

		# Draw x and y lists
		plt.cla()

		ax[0].clear()
		ax[1].clear()
		ax[2].clear()

		#ax.clear()
	
		ax[0].plot(xs, lidar_readings)
		ax[0].title.set_text('Lidar Readings')
		ax[0].set_ylabel('Distance (cm)')
		ax[0].annotate(lidar_readings[19], (xs[19], lidar_readings[19]), xytext=(xs[19], lidar_readings[19]))

		ax[1].plot(xs, ultra_right_readings)
		ax[1].title.set_text('Ultra_left Readings')
		ax[1].set_ylabel('Distance (cm)')
		ax[1].annotate(ultra_right_readings[19], (xs[19], ultra_right_readings[19]), xytext=(xs[19], ultra_right_readings[19]))

		ax[2].plot(xs, ultra_left_readings)
		ax[2].title.set_text('Ultra_right Readings')
		ax[2].set_ylabel('Distance (cm)')
		ax[2].annotate(ultra_left_readings[19], (xs[19], ultra_left_readings[19]), xytext=(xs[19], ultra_left_readings[19]))
		plt.draw()
		# Format plot
		#plt.xticks(rotation=45, ha='right')
		#plt.subplots_adjust(bottom=0.30)
		plt.pause(0.01)
		
		#time.sleep(0.5)
		

	
def initialise_arrays():
	global lidar_readings
	global ultra_right_readings
	global ultra_left_readings
	global xs
	xs = np.linspace(0, 6*np.pi, 20)
	lidar_readings = np.zeros(20).tolist()
	ultra_right_readings = np.zeros(20).tolist()
	ultra_left_readings = np.zeros(20).tolist()


#If name = main
if __name__ == '__main__':
	thread = threading.Thread(target=sub_loop, daemon=True)
	thread.start()
	initialise_arrays()
	#thread2 = threading.Thread(target=plotting, daemon=True)
	#thread2.start()
	#plt.show()
	#thread2 = threading.Thread(target=plotting, daemon=True)
	#thread2.start()
	#ani = animation.FuncAnimation(fig, plotting, fargs=(xs, ys), interval=1000)
	plotting()
	
	while True:
		pass
	
