from flask import render_template
from config import socket_app, app
from sockets import SocketClass


@app.route('/')
def index():
    return render_template('index.html', async_mode=socket_app.async_mode)


socket_app.on_namespace(SocketClass('/'))


if __name__ == '__main__':
    socket_app.run(app)
