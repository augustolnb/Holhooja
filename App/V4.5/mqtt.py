topic = '/esp32/verificarConexao'
topic2 = '/esp32/enviarComando'

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    #print(topic)
    print("Menssagem recebida do tópico: ", topic)
    print("Messagem:", payload)

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Conectado ao broker MQTT")
        client.subscribe(topic)
        client.subscribe(topic2)
        print("Inscrito nos tópicos: ")
        print(topic)
        print(topic2)
    else:
        print("Conexão falhou, reason_code: " + str(reason_code))


def on_publish(client, userdata, mid, reason_code, properties):
    print("Dados publicados \n")
    pass
