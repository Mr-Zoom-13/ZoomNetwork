from flask import Flask, request, render_template
from threading import Lock
from flask_socketio import SocketIO, Namespace, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_config_secret_zoom'
async_mode = None
socket_app = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()


@app.route('/')
def index():
    return render_template('index.html', async_mode=socket_app.async_mode)


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


socket_app.on_namespace(SocketClass('/'))


if __name__ == '__main__':
    socket_app.run(app)
