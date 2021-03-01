import paho.mqtt.client as paho

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    print(msg.payload)
    if('pi:' in str(msg.payload)):
        print("Good Message: "+ str(msg.payload))
        exit()

def sub_loop():
    client = paho.Client()
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.connect('broker.mqttdashboard.com', 1883)
    client.subscribe('FYP_Mqtt_Messaging/Pi', qos=1)

    client.loop_forever()
