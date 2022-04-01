import os
from flask import Flask
from flask_session import Session
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from app.config import AppConfig


app = Flask(__name__)
app.config.from_object(AppConfig)
Session(app)
db = SQLAlchemy(app)
db.create_all()
login_manager = LoginManager()
login_manager.init_app(app)


from app import routes  # noqa: F401, E402
