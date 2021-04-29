import paho.mqtt.client as paho
import motor_controller as mc
import time

##Print out when subscribed succesfully
def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

##What to do for each message
def on_message(client, userdata, msg):
    #Print the message details
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    print(msg.payload)
    #Check message contents
    if('forward' in str(msg.payload)):
        print("moving forward")
        mc.forward()
        time.sleep(.75)
        mc.stop()
    elif('back' in str(msg.payload)):
        print("moving back")
        mc.back()
        time.sleep(.75)
        mc.stop()
    elif('right' in str(msg.payload)):
        print("moving right")
        mc.right()
        time.sleep(.25)
        mc.stop()
    elif('left' in str(msg.payload)):
        print("moving left")
        mc.left()
        time.sleep(.25)
        mc.stop()
    elif('pi:' in str(msg.payload)):
        print("Good Message: "+ str(msg.payload))
        exit()

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
