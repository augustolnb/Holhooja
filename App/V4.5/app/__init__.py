from flask import Flask
from config import Config
from threading import Lock
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt
from mqtt import on_connect, on_message, on_publish

async_mode = None
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

###################
#   MQTT CONFIG   #
###################
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
#####################################

print('Iniciando servidor socket')
socketio = SocketIO(app, async_mode=async_mode)
login = LoginManager(app)
thread = None
thread_lock = Lock()

from app import routes, models

# Flask_Mqtt

#from flask_mqtt import Mqtt
"""
topic = '/esp32/verificarConexao'
mqtt_client = Mqtt(app)
app.config['MQTT_BROKER_URL'] = '192.168.100.212'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_PASSWORD'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_KEEPALIVE'] = 5  # Set KeepAlive time in seconds
app.config['MQTT_TLS_ENABLED'] = False  # If your server supports TLS, set it True
"""

if __name__ == '__main__':
    socketio.run(app)
