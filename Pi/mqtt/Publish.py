##Script to be imported to publish data on MQTT topic
##Imports
import paho.mqtt.client as paho
import time

##On publish print sent as a confirmation
def on_publish(client, userdata, mid):
    print("sent")
 
##Send data to the topic under Pi/Remote unless specified
def send(data,location='Pi/Remote'):
    ##Create a client
    client = paho.Client()
    ##Setup up the confirmation method
    client.on_publish = on_publish
    ##Establish a connection to the broker
    client.connect('broker.mqttdashboard.com', 1883)
    ##Connect the client
    client.loop_start()
    ##Publish the data as a string to the topic under the directory given (default Pi/Remote)
    (rc, mid) = client.publish("FYP_Mqtt_Messaging/"+location,str(data), qos=1)
    ##Wait a small amount for data to be available
    time.sleep(0.1)
