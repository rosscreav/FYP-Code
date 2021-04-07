from flask_socketio import SocketIO
from flask import Flask, render_template
from threading import Thread, Event
##Mqtt file for sending data
from pythonfiles import Publish as p
##Python script to query datanase
from pythonfiles import firebase_query

app = Flask(__name__)
app.config['DEBUG'] = True

# turn the flask app into a socketIO app
socketIO = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

# Thread
thread = Thread()
thread_stop_event = Event()

#Get the data from firebase and use it to update the chart
def update_chart_data():
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
    data.reverse()
    times.reverse()
    data_dict = {"data": data, "labels": times, "legend": legend}
    #Send the data to the javascript
    socketIO.emit('update', data_dict, namespace='/test')
    #Wait 5 seconds
    socketIO.sleep(5)


##Route index to main webpage
@app.route('/')
def index():
    # only by sending this page first will the client be connected to the socketio instance
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
