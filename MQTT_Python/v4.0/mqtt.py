import mariadb
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

# Database connection details
DB_HOST = "localhost"
DB_NAME = "test"
DB_USER = "augusto"
DB_PASSWORD = "1234"

# MQTT connection details
broker_address = "192.168.100.168"
broker_port = 1883

# MQTT topics
topicEspAr = "/comandos/esp32/ar"
topicEspPorta = "/comandos/esp32/porta"
topicSensorDHT = "/sensores/DHT"
topicSensorLDR = "/sensores/LDR"
topicSensorSR602 = "/sensores/SR602"

def connect_to_database():
    """Connects to the MariaDB database and returns the connection object."""
    try:
        conn = mariadb.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def store_dht_in_database(umidade, temperatura):

    conn = connect_to_database()

    if conn:
        cursor = conn.cursor()

        sql_update = "UPDATE sensores SET umidade = ?, temperatura = ? WHERE id_sensores = 1"
        values = (umidade, temperatura)
        
        try:
            cursor.execute(sql_update, values)
            conn.commit()
            print("Data stored successfully!")
        except mariadb.Error as e:
            print(f"Error storing data: {e}")

        conn.close()

def store_ldr_in_database(luminosidade):

    conn = connect_to_database()

    if conn:
        cursor = conn.cursor()

        sql_update = "UPDATE sensores SET luminosidade = ? WHERE id_sensores = 1"
        values = (luminosidade)
        
        try:
            cursor.execute(sql_update, values)
            conn.commit()
            print("Data updated successfully!")
        except mariadb.Error as e:
            print(f"Error updating data: {e}")

        conn.close()

def store_sr602_in_database(movimento):
    conn = connect_to_database()

    if conn:
        cursor = conn.cursor()

        sql_update = "UPDATE sensores SET movimento = ? WHERE id_sensores = 1"
        values = (movimento)
        
        try:
            cursor.execute(sql_update, values)
            conn.commit()
            print("Data updated successfully!")
        except mariadb.Error as e:
            print(f"Error updating data: {e}")

        conn.close()

def on_message(client, userdata, msg):

    topic = msg.topic
    payload = msg.payload.decode()
    #print(topic)
    print("Received message on topic:", topic)
    print("Message:", payload)
    if topic == topicSensorDHT:
        # Converte a string recebida em um dicionario paitu
        payload = eval(payload)
        valores = []    

        # Anexa os valores enviados em uma lista
        for i in payload.values():
            valores.append(i)

        #store_data_in_database(umidade, temperatura)
        store_dht_in_database(valores[0], valores[1])

    elif topic == topicSensorLDR:
        # Converte a string recebida em um dicionario paitu
        payload = eval(payload)
        valores = []    

        # Anexa os valores enviados em uma lista
        for i in payload.values():
            valores.append(i)

        #store_data_in_database(umidade, temperatura)
        store_ldr_in_database(valores)
    
    elif topic == topicSensorSR602:
        # Converte a string recebida em um dicionario paitu
        payload = eval(payload)
        valores = []    

        # Anexa os valores enviados em uma lista
        for i in payload.values():
            valores.append(i)

        #store_data_in_database(umidade, temperatura)
        store_sr602_in_database(valores)

def on_connect(client, userdata, flags, reason_code, properties):
    """Checks the MQTT connection status."""
    if reason_code == 0:
        print("Connected to MQTT broker")
        client.subscribe(topicSensorDHT)
        client.subscribe(topicSensorLDR)
        client.subscribe(topicSensorSR602)
        print("Inscrito nos tópicos: ")
        print(topicSensorDHT)
        print(topicSensorLDR)
        print(topicSensorSR602)
    else:
        print("Failed to connect, reason_code: " + str(reason_code))

def clear_table(conn):
    cursor = conn.cursor()

    cursor.execute("DELETE FROM sensores;")
    conn.commit()

    print("Table cleared successfully!")

if __name__ == "__main__":
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.connect(broker_address, broker_port)
    client.on_message = on_message

    client.loop_forever()
