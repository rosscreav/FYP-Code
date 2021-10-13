##Script based on UDP_Remote_Control to allow remote control of motors using MQTT messages
##Imports
import paho.mqtt.client as paho
import motor_controller as mc
import time

##Print out when subscribed succesfully
def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

##Method to decode instructions into commands (called every time a message is recieved)
##All movements are for .75s and then stopped
def on_message(client, userdata, msg):
    #Print the message details
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    print(msg.payload)
    #Check message contents
    ##Forward
    if('forward' in str(msg.payload)):
        print("moving forward")
        mc.forward()
        time.sleep(.75)
        mc.stop()
    ##Back
    elif('back' in str(msg.payload)):
        print("moving back")
        mc.back()
        time.sleep(.75)
        mc.stop()
    ##Right
    elif('right' in str(msg.payload)):
        print("moving right")
        mc.right()
        time.sleep(.20)
        mc.stop()
    ##Left
    elif('left' in str(msg.payload)):
        print("moving left")
        mc.left()
        time.sleep(.20)
        mc.stop()
    ##Shutdown
    elif('pi:' in str(msg.payload)):
        print("Good Message: "+ str(msg.payload))
        exit()

##Keep looping for messages and execute on_message on recieving a messgae
def sub_loop():
    ##Create a connection using paho
    client = paho.Client()
    ##Set on subscribe and on message functions
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    ##Create a connection to my MQTT server
    client.connect('broker.mqttdashboard.com', 1883)
    client.subscribe('FYP_Mqtt_Messaging/Pi/Remote', qos=1)
    ##Loop until script is closed
    client.loop_forever()

#If name = main call main method
if __name__ == '__main__':
    sub_loop()
