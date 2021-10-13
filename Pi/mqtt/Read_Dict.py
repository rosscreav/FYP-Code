##A script to read the MQTT sensor stream and live plot the data (Demo_Send_Data client)
##Improts
import paho.mqtt.client as paho
import numpy as np
import json
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading

##Array to hold the valus in the plot
lidar_readings = []
ultra_right_readings = []
ultra_left_readings =[]

##Create a figure with 3 subplots for each sensor
fig, ax = plt.subplots(nrows=3, ncols=1)
fig.tight_layout()
##Array to hold x values for the readings
xs = []

##Print out when subscribed succesfully (MQTT)
def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

##What to do with each message (add to to the plot values)
def on_message(client, userdata, msg):
	##Use the global arrays
	global lidar_readings
	global ultra_right_readings
	global ultra_left_readings

	##If the message does not contain sensor data ignore it
	if "lidar" not in str(msg.payload):
		print("passing")
		return 
	##Decode the string to UTF and replace ' with " to allow json conversion
	string = msg.payload.decode('UTF-8').replace("'",'"')
	##Print the data to console
	print(string)
	##Convert the value to a dictionary
	dict_val = json.loads(string)

	##Print the lidar value
	print("lidar " + str(dict_val["lidar"]))
	##Add the data to a global array of plot values
	lidar_readings.append(float(dict_val["lidar"]))
	##Pop the last value to maintain plot size
	lidar_readings.pop(0)

	##Print the right ultrasound value
	print("ultra_right " + str(dict_val["ultra_right"]))
	##Add the data to a global array of plot values
	ultra_right_readings.append(float(dict_val["ultra_right"]))
	##Pop the last value to maintain plot size
	ultra_right_readings.pop(0)

	##Print the left ultrasound value
	print("ultra_left " + str(dict_val["ultra_left"]))
	##Add the data to a global array of plot values
	ultra_left_readings.append(float(dict_val["ultra_left"]))
	##Pop the last value to maintain plot size
	ultra_left_readings.pop(0)

	##Print out the time stamp at the end of the value print out and leave a gap
	print("timestamp " + str(dict_val["timestamp"]))
	print("\n")

##Listener loop
def sub_loop():
    ##Create a client
    client = paho.Client()
    ##Declare on message and on subscribe methods as above
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    ##Connect to the broke and establish a connection to my topic
    client.connect('broker.mqttdashboard.com', 1883)
    client.subscribe('FYP_Mqtt_Messaging/Pi', qos=1)
    ##Loop until script is ended
    client.loop_forever()

##Method for live plotting of the data (must be on main thread)
def plotting():
	##Loop until script ends
	while True:
		##Clear all on the plot
		plt.cla()

		##Clear the axis of each plot
		ax[0].clear()
		ax[1].clear()
		ax[2].clear()
	
		##Lidar plot
		##Plot graph
		ax[0].plot(xs, lidar_readings)
		##Set the name
		ax[0].title.set_text('Lidar Readings')
		##Give the units
		ax[0].set_ylabel('Distance (cm)')
		##Add annotation on the last point of the graph (most recent datapoint)
		ax[0].annotate(lidar_readings[19], (xs[19], lidar_readings[19]), xytext=(xs[19], lidar_readings[19]))

		##Right ultrasound plot
		##Plot graph
		ax[1].plot(xs, ultra_right_readings)
		##Set the name
		ax[1].title.set_text('Ultra_left Readings')
		##Give the units
		ax[1].set_ylabel('Distance (cm)')
		##Add annotation on the last point of the graph (most recent datapoint)
		ax[1].annotate(ultra_right_readings[19], (xs[19], ultra_right_readings[19]), xytext=(xs[19], ultra_right_readings[19]))

		##Left ultrasound plot
		##Plot graph
		ax[2].plot(xs, ultra_left_readings)
		##Set the name
		ax[2].title.set_text('Ultra_right Readings')
		##Give the units
		ax[2].set_ylabel('Distance (cm)')
		##Add annotation on the last point of the graph (most recent datapoint)
		ax[2].annotate(ultra_left_readings[19], (xs[19], ultra_left_readings[19]), xytext=(xs[19], ultra_left_readings[19]))
		##Draw the plot to screen
		plt.draw()
		##Wait 0.01s and redraw
		plt.pause(0.01)
		
##Init the arry values to 0
def initialise_arrays():
	##Call the global array variables
	global lidar_readings
	global ultra_right_readings
	global ultra_left_readings
	global xs
	##Create a 20 long array with equally spaced points for x axis
	xs = np.linspace(0, 6*np.pi, 20)
	##Init all other arrays to 20 0's
	lidar_readings = np.zeros(20).tolist()
	ultra_right_readings = np.zeros(20).tolist()
	ultra_left_readings = np.zeros(20).tolist()


#If name = main
if __name__ == '__main__':
	##Create a thread to handle the MQTT reading and start it
	thread = threading.Thread(target=sub_loop, daemon=True)
	thread.start()
	##Initialise up the arrays
	initialise_arrays()
	##Start plotting the data
	plotting()
	
