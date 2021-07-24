"""The user class"""
import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    """The user class"""
    def __init__(self, username, name, email, password, date_created = None, date_modified = None):
        self.username = username
        self.name = name
        self.email = email
        self.password = password

        if date_created is None:
            self.date_created = datetime.datetime.now().strftime("%B %d %Y - %H:%M")
        else:
            self.date_created = date_created

        if date_modified is None:
            self.date_modified = datetime.datetime.now().strftime("%B %d %Y - %H:%M")
        else:
            self.date_modified = date_modified

    def __repr__(self):
        return f'<User: {self.username}>'

    def get_id(self):
        return self.username

    def get(username):
        if username == username:
            return self
        return None

    def set_hashed_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha512:100')

    def check_password(self, secret):
        return check_password_hash(self.password, secret)