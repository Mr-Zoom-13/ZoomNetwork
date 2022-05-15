from config import thread_lock, socket_app, thread
from flask import request
from flask_socketio import SocketIO, Namespace, emit


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socket_app.sleep(10)
        count += 1
        socket_app.emit('my_response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/test')


class SocketClass(Namespace):
    def on_connect(self):
        global thread
        with thread_lock:
            if thread is None:
                thread = socket_app.start_background_task(background_thread)
        print('Client connected', request.sid)
        emit('my_response', {'data': 'Connected', 'count': 0})

    def on_disconnect(self):
        print('Client disconnected', request.sid)