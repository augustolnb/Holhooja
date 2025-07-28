import mariadb

# Database connection details
DB_HOST = "localhost"
DB_NAME = "sql_db"
DB_USER = "augusto"
DB_PASSWORD = "1234"

# MQTT connection details
broker_address = "192.168.100.212"
broker_port = 1883

# Topicos MQTT
#topic = '/esp32/verificarConexao' 
#topic2 = '/esp32/enviarComando'
topicSensorDHT = "/sensores/DHT"; # subscribe
topicSensorLDR = "/sensores/LDR"; # subscribe
topicSensorSR602 = "/sensores/SR602"; # subscribe

### Estabelece conexão com o BD
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

### Funções para manipulação de dados no BD
def store_dht_in_database(umidade, temperatura):

    conn = connect_to_database()

    if conn:
        cursor = conn.cursor()

        sql_update = "UPDATE sensores SET umidade = ?, temperatura = ? WHERE id = 1"
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

        sql_update = "UPDATE sensores SET luminosidade = ? WHERE id = 1"
        values = (luminosidade)
        
        try:
            cursor.execute(sql_update, values)
            conn.commit()
            print("Data updated successfully!")
        except mariadb.Error as e:
            print(f"Error updating data: {e}")

        conn.close()

# MUDAR NOME DO SENSOOORRRR
def store_sr602_in_database(movimento):
    conn = connect_to_database()

    if conn:
        cursor = conn.cursor()

        sql_update = "UPDATE sensores SET movimento = ? WHERE id = 1"
        values = (movimento)
        
        try:
            cursor.execute(sql_update, values)
            conn.commit()
            print("Data updated successfully!")
        except mariadb.Error as e:
            print(f"Error updating data: {e}")

        conn.close()


#############################################

######### FUNÇÕES DE CALLBACK DO MQTT
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    print("Mensagem recebida no tópico: ", topic)
    #print("Messagem: ", payload)

    # Atualização dos dados dos sensores no BD

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
    if reason_code == 0:
        print("Conectado ao broker MQTT")
        #client.subscribe(topic)
        #client.subscribe(topic2)
        client.subscribe(topicSensorDHT)
        client.subscribe(topicSensorLDR)
        client.subscribe(topicSensorSR602)
        print("Inscrito nos tópicos: ")
        print(topicSensorDHT +'\n'+ topicSensorLDR +'\n'+ topicSensorSR602)
    else:
        print("Conexão falhou, reason_code: " + str(reason_code))


def on_publish(client, userdata, mid, reason_code, properties):
    print("Dados publicados \n")
    pass
