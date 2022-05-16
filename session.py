from flask import session


class WorkWithSession():
    def set_new_value(self, key, value):
        session[key] = value

    def get_value(self, key):
        return session[key]
