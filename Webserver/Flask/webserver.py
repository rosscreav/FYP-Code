from flask_socketio import SocketIO
from flask import Flask, render_template
from threading import Thread, Event
##Mqtt file for sending data
from pythonfiles import Publish as p
##Python script to query datanase
from pythonfiles import firebase_query
import matplotlib.pyplot as plt
import numpy as np
import math
from firebase import firebase


app = Flask(__name__)
app.config['DEBUG'] = True

# turn the flask app into a socketIO app
socketIO = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

# Thread
thread = Thread()
thread_stop_event = Event()

#Get the data from firebase and use it to update the chart
def update_chart_data():
    while True:
        #inputs for the js
        legend = 'Lidar Readings'
        data = []
        times = []
        #Query the database
        database = firebase_query.get_most_recent_data()
        for entry in database:
            times.append(entry['timestamp'])
            data.append(entry['lidar'])
        #Reverse to show newest data on the right
        ultra_left = database[0]['ultra_left']
        ultra_right = database[0]['ultra_right']
        lidar_value = database[0]['lidar']
        data.reverse()
        times.reverse()
        data_dict = {"data": data, "labels": times, "legend": legend}
        #Send the data to the javascript
        socketIO.emit('update', data_dict, namespace='/test')
        socketIO.emit('ultra_left', str(ultra_left)+"cm", namespace='/test')
        socketIO.emit('ultra_right', str(ultra_right)+"cm", namespace='/test')
        socketIO.emit('lidar_value', str(lidar_value)+"cm", namespace='/test')
        #Wait 5 seconds
        socketIO.sleep(5)


##Route index to main webpage
@app.route('/')
def index():
    # only by sending this page first will the client be connected to the socketio instance
    return render_template('livelidar.html')

##Route index to threading
@app.route('/test')
def index1():
    # only by sending this page first will the client be connected to the socketio instance
    MapData = get_most_recent_data()
    plot(MapData)
    return render_template('livelidar.html')

##Route to mqtt hmtl file
@app.route('/MQTTControl')
def index2():
    return render_template('mqttcontrol.html')

##On connection the test webpage starts a thread to update the chart every 5s
@socketIO.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    # Start the thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = socketIO.start_background_task(update_chart_data)

##Send message from javascript socket
@socketIO.on('message')
def mqqt_message(data):
    #Using MQTT script send mqtt button press
    p.send(data)

##Print disconnect to console
@socketIO.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

##Run webstie
if __name__ == '__main__':
    socketIO.run(app)

##Plotting
def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

def plot(input):
    input= list(filter((-3).__ne__, input))
    angle = 360/len(input)
    curangle = 0
    x=[]
    y=[]
    for dist in input:
        if dist != -3:
            x.append((dist+18) * math.cos(math.radians(curangle)))
            y.append((dist+18) * math.sin(math.radians(curangle)))
        curangle+= angle
    #yhat = np.convolve(y, box, mode='same')
    plt.cla()
    plt.scatter(x, smooth(y,3))
    plt.scatter([0],[0],color='red')
    plt.text(0, 0+2, 'Robot Postion')
    plt.savefig('./static/images/map.png')

def get_most_recent_data():
    fb = firebase.FirebaseApplication("https://fyp-database-7e287-default-rtdb.europe-west1.firebasedatabase.app/",None)

    MapData = []

    db_entries = fb.get('./MapData/',None)
    db_entries = list(db_entries.values())
    db_entries.reverse()
    for entry in db_entries[0]:
        MapData.append(entry)
    return MapData

