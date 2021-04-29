import paho.mqtt.client as paho

import json
import time


##Print out when subscribed succesfully
def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

##What to do for each message
def on_message(client, userdata, msg):

	if "lidar" not in str(msg.payload):
		print("passing")
		return 
	#Print the message details
	print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
	print(str(msg.payload))
	dict_val = json.loads(str(msg.payload))
	print("lidar " + str(dict_val["lidar"]))
	print("ultra_right " + str(dict_val["ultra_right"]))
	print("ultra_left " + str(dict_val["ultra_left"]))
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

#If name = main
if __name__ == '__main__':
    sub_loop()
