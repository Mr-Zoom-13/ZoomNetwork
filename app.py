from flask import render_template, redirect, request
from flask_login import login_user, current_user, login_required, logout_user
from config import socket_app, app, db_ses, login_manager, work_with_session
from sockets import SocketClass
from forms.login import LoginForm
from forms.register import RegisterForm
from data.users import User


@login_manager.user_loader
def load_user(user_id):
    return db_ses.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db_ses.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            work_with_session.set_new_value('id', user.id)
            print('FFFFFF', work_with_session.get_value('id'))
            return redirect(f'/main/{work_with_session.get_value("id")}')
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, user=current_user)
    return render_template('login.html', form=form, user=current_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            if form.password.data != form.password_again.data:
                return render_template('register.html',
                                       form=form,
                                       message="Пароли не совпадают", user=current_user)
            elif int(form.age.data) <= 0:
                return render_template('register.html',
                                       form=form,
                                       message="Неверный возраст", user=current_user)
            elif db_ses.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html',
                                       form=form,
                                       message="Аккаунт с данной почтой уже зарегистрирован",
                                       user=current_user)
        except ValueError:
            return render_template('register.html',
                                   form=form,
                                   message="Неверный возраст", user=current_user)
        user = User(email=form.email.data, surname=form.surname.data, name=form.name.data,
                    age=form.age.data)
        user.set_password(form.password.data)
        db_ses.add(user)
        db_ses.commit()
        this_user = db_ses.query(User).filter(User.email == form.email.data).first()
        print(this_user.id)
        login_user(this_user)
        work_with_session.set_new_value('id', this_user.id)
        return redirect(f'/main/{work_with_session.get_value("id")}')
    return render_template('register.html', form=form, user=current_user)


@app.route('/main/<int:id>', methods=['GET', 'POST'])
@login_required
def profile(id):
    user = db_ses.query(User).filter(User.id == id).first()
    if request.method == 'POST':
        if 'my_prof' in request.form:
            return redirect(f'/main/{work_with_session.get_value("id")}')
    print(work_with_session.get_value("id"))
    if user.id == work_with_session.get_value("id"):
        return render_template('profile.html', user=user, owner=True)
    return render_template('profile.html', user=user, owner=False)


if __name__ == '__main__':
    for i in db_ses.query(User).all():
        i.sid = '[]'
    socket_app.on_namespace(SocketClass('/main'))
    socket_app.run(app, debug=True)
