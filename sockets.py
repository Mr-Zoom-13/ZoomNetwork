from config import thread_lock, socket_app, thread, db_ses, work_with_session
from flask import request
from flask_socketio import Namespace, emit
from data.users import User
import datetime


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

    def on_disconnect(self):
        print('Client disconnected', request.sid)

    def on_add_sid(self):
        id = work_with_session.get_value('id')
        print(id)
        user = db_ses.query(User).filter(User.id == id).first()
        user.last_seen = 'online'
        if not user.sid:
            temp_sid = [request.sid]
        else:
            temp_sid = eval(user.sid)
            if request.sid not in temp_sid:
                temp_sid.append(request.sid)
        user.sid = str(temp_sid)
        db_ses.commit()
        emit('user_update', {'data': user.id, 'last_seen': user.last_seen}, broadcast=True)

    def on_delete_sid(self):
        id = work_with_session.get_value('id')
        print(id)
        user = db_ses.query(User).filter(User.id == id).first()
        tmp_sid = eval(user.sid)
        index_delete = tmp_sid.index(request.sid)
        del tmp_sid[index_delete]
        user.sid = str(tmp_sid)
        if not tmp_sid:
            user.last_seen = str(datetime.date.today())
        db_ses.commit()