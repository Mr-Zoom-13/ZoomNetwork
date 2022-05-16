from flask import Flask
from flask_login import LoginManager
from flask_socketio import SocketIO
from threading import Lock
from data import db_session

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'my_config_secret_zoom'
async_mode = None
socket_app = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()
db_session.global_init('db/network.db')
db_ses = db_session.create_session()
login_manager = LoginManager()
login_manager.init_app(app)