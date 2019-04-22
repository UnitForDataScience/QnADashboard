from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send
from persistqueue import Queue
import time, threading
from threading import Lock
from summary_models import summarize_tf, summarize_page_rank

task_queue = Queue('./queue')

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1048576
socketio = SocketIO(app, async_mode='threading')

thread = None
thread_lock = Lock()
clients = set()


def request_thread_reader():
    while True:
        if task_queue.qsize():
            task = task_queue.get()
            if task['sid'] in clients:
                if task['type'] == 'summarize':
                    if task['summary_type'] == 'page_rank':
                        task['summary'] = summarize_page_rank(task['text'],
                                                              keywords=task['keywords'] if 'keywords' in task else [],
                                                              count=task['n'])
                    else:
                        task['summary'] = summarize_tf(task['text'],
                                                       keywords=task['keywords'] if 'keywords' in task else [],
                                                       count=task['n'])
                sid = task['sid']
                del task['sid']
                del task['text']
                socketio.emit('message', task, room=sid)
            task_queue.task_done()
        else:
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
    clients.add(request.sid)
    task_queue.put(data)


@socketio.on('disconnect')
def disconnect():
    if request.sid in clients:
        clients.remove(request.sid)
    print('Someone disconnected')


if __name__ == '__main__':
    socketio.run(app, port=8000, debug=True, host='0.0.0.0')
