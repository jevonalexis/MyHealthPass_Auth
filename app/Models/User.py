from app import db
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    locked = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, email, password, firstname='', lastname=''):
        self.email = email
        self.password = password
        self.firstname = firstname
        self.lastname = lastname

    def get_id(self):
        return f'{self.user_id}'

    def __repr__(self):
        return f"<User {self.email} {'locked' if self.locked else 'unlocked'}>"
