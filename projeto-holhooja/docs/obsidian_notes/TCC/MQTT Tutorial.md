
________________________________________________________________________
**Links**
- http://www.steves-internet-guide.com/mqtt-tools/
- https://aws.amazon.com/pt/what-is/mqtt/#:~:text=MQTT%20is%20a%20standards-based,constrained%20network%20with%20limited%20bandwidth
- https://alfacomp.net/2022/03/24/mqtt-conheca-o-protocolo-padrao-do-iot/

*Brokers públicos:* https://www.newtoncbraga.com.br/microcontroladores/143-tecnologia/17117-comunicando-se-via-mqtt-com-o-esp32-mic404.html

*Mosquitto Password:* https://mosquitto.org/man/mosquitto_passwd-1.html
________________________________________________________________________

### Free Online Broker

- test.mosquitto.org
- broker.hivemq.com
- iot.eclipse.org

### Main Client Methods

- connect() and disconnect()
- subscribe() and unsubscribe()
- publish()

Each of these methods is associated with a **callback.**


### How To Install

- **sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa**
- **sudo apt-get update**
- **sudo apt-get install mosquitto**
- **sudo apt-get install mosquitto-clients**
- **sudo apt clean**

### Checking Open Doors

O netstat lista as portas abertas TCP/UDP:
```sh
$ netstat -tunl
```
O netstat com a opção -p mostra os processos donos das portas.
```sh
$ sudo netstat -tunlp
```
O comando ss também pode mostrar as portas abertas com a opção idêntica:
```sh
ss -tunelp
```
Para verificar se as portas 1883 estão sendo utilizadas
```sh
sudo lsof -i | grep 1883
ss -tunelp | grep 1883
```
Formas de manipular o serviço:
```sh
systemctl start mosquitto.service
systemctl stop mosquitto.service
systemctl restart mosquitto.service
```


### Useful Linux Commands

```sh
ps -aux | grep mosquitto  
pgrep mosquitto  
kill -9 PID (that you get from above command)
```

### Conectando e Recebendo Mensagens

Inicia o serviço em foreground
```
mosquitto -v
```

*mosquitto_sub -h endereço -p porta -t topico_inscrito*
```
mosquitto_sub -h localhost -p 1883 -t 'temperatura'
```




### Bug MQTT.CLIENT()  version1 x version2
________________________________________________________________________
**Links:**
- https://stackoverflow.com/questions/77984857/paho-mqtt-unsupported-callback-api-version-error

- https://eclipse.dev/paho/files/paho.mqtt.python/html/migrations.html
________________________________________________________________________
Passagem de parâmetros da versão 1:
```python
client = mqtt_client.Client(client_id)
```
Passagem de parâmetros da versão 2:
```python
client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
```

This will configure the library to use the v1 callback API (as used with older versions of the library). I would recommend reading the document linked above and planning to migrate to `CallbackAPIVersion.API_VERSION2`.

An alternative option would be to install a v1 release (v1.6.1 is the latest; `pip install paho-mqtt<2.0.0` will install this). V2 does include quite a few fixes/enhancements so it is worth considering using that version.

### CONNECT packet & CONNACK response

When you send mqtt CONNECT packet, you should receive CONNACK response. This response contains the following codes

>0 - success, connection accepted
1 - connection refused, bad protocol
2 - refused, client-id error
3 - refused, service unavailable
4 - refused, bad username or password
5 - refused, not authorized

As you can see, your response should be 4. But it is zero. It might be that you broker doesn't check credentials so your connect message is accepted. Client looks fine.