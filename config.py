from flask import Flask
from flask_socketio import SocketIO
from threading import Lock

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_config_secret_zoom'
async_mode = None
socket_app = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()
