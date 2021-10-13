##Script to subscribe to a topic
##Imports
import paho.mqtt.client as paho

##Upon creating the connect print info to console
def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

##When a message arrives check the string and print good messages
def on_message(client, userdata, msg):
    ##Print full message to console
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    ##Print the message content alone
    print(msg.payload)
    ##If pi: in the message shut down 
    if('pi:' in str(msg.payload)):
        ##Print to console and shut down script
        print("Good Message: "+ str(msg.payload))
        exit()

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
