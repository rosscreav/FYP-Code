import paho.mqtt.client as paho
import time

def on_publish(client, userdata, mid):
    print("sent")
 
def send(data):
    client = paho.Client()
    client.on_publish = on_publish
    client.connect('broker.mqttdashboard.com', 1883)
    client.loop_start()
    (rc, mid) = client.publish("FYP_Mqtt_Messaging/Pi",str(data), qos=1)
    time.sleep(0.1)
