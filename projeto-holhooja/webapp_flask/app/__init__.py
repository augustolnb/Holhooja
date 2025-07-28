from flask import Flask
from config import Config 
from threading import Lock
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt
from mqtt import on_connect, on_message, on_publish

async_mode = None # Modo de sincronia do socket 
app = Flask(__name__) # Declaração do objeto app
app.config.from_object(Config) # Configuração do objeto app segundo o arquivo Config
db = SQLAlchemy(app) # Declaração do objeto db para manipulação do banco de dados

#   MQTT CONFIG   #
# paho.mqtt.client
broker_address = "192.168.100.212"
broker_port = 1883

# Configuração do cliente mqtt
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.connect(broker_address, broker_port)

print('Iniciando loop MQTT')
client.loop_start()

print('Iniciando servidor socket')
socketio = SocketIO(app, async_mode=async_mode)
login = LoginManager(app)
thread = None
thread_lock = Lock()

from app import routes, models

if __name__ == '__main__':
    socketio.run(app)
