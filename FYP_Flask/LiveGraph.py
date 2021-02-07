from flask_socketio import SocketIO
from flask import Flask, render_template
from threading import Thread, Event
import firebase_query

app = Flask(__name__)
app.config['DEBUG'] = True

# turn the flask app into a socketIO app
socketIO = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

# Thread
thread = Thread()
thread_stop_event = Event()


def update_chart_data():
    while not thread_stop_event.isSet():
        legend = 'Lidar Readings'
        data = []
        times = []
        database = firebase_query.get_most_recent_data()
        for entry in database:
            times.append(entry['timestamp'])
            data.append(entry['lidar'])
        data.reverse()
        times.reverse()
        data_dict = {"data": data, "labels": times, "legend": legend}
        # print(data)
        # print("Updating : "+str(data_dict))
        socketIO.emit('update', data_dict, namespace='/test')
        socketIO.sleep(5)


@app.route('/')
def index():
    # only by sending this page first will the client be connected to the socketio instance
    return render_template('livelidar.html')


@socketIO.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    # Start the thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = socketIO.start_background_task(update_chart_data)


@socketIO.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketIO.run(app)
