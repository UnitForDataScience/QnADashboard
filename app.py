from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send
from persistqueue import Queue
import time, threading
from threading import Lock

task_queue = Queue('./queue')

app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')


thread = None
thread_lock = Lock()


def request_thread_reader():
    while True:
        if task_queue.qsize():
            task = task_queue.get()
            socketio.emit('message', task)
            task_queue.task_done()
        time.sleep(1)


t1 = threading.Thread(target=request_thread_reader)
t1.start()


@app.route('/polls/')
def hello_world():
    return render_template('index.html')


@socketio.on('connected')
def connected():
    print('Someone connected')


@socketio.on('request')
def handle_request(data):
    data['sid'] = request.sid
    task_queue.put(data)


@socketio.on('disconnect')
def disconnect():
    print('Someone disconnected')


if __name__ == '__main__':
    socketio.run(app, port=8000, debug=True, host='0.0.0.0')
