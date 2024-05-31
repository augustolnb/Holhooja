from flask import Flask
from config import Config
from threading import Lock
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

async_mode = None

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

from app import routes, models

if __name__ == '__main__':
    socketio.run(app)
