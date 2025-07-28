#include "DHTStable.h"
#include "holhooja.h"
#include <Arduino.h>
#include <IRrecv.h>
#include <IRutils.h>
#include <IRsend.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include "EmonLib.h"

EnergyMonitor emon1;

//  DEFINIÇÃO DAS CONSTANTES

const int MovementTimer = 4000;  // 4s
const int DHT11_PIN = 21;
const int DHTReadTimer = 8000;  // 8s
const int MQ135ReadTimer = 8000;  // 8s
const int SCTReadTimer = 8000;  // 8s
const int led = 18;
const int MQ135_D_PIN = 2;
const int MQ135_A_PIN = 1;
const int LDR_PIN = 20;
const int LDRReadTimer = 8000;  // 8s
const int kRecvPin = 10;
const int sctPin = 18;
const int motionSensor = 19;
const uint8_t kTimeout = 50;
const uint16_t kSendIRLed = 40;
const uint16_t kCaptureBufferSize = 1024;
const int RelePin = 15;

// CONSTANTES DE CONEXÃO MQTT
IPAddress mqtt_server(192, 168, 137, 57); 
const int mqtt_port = 1883;

// CONSTANTES DE CONEXÃO WIFI
const char *ssid = "holhooja";
const char *password = "testelpa";

// CRIAÇÃO DOS OBJETOS DE CADA CLASSE
DHTStable DHT;
IRrecv irrecv(kRecvPin, kCaptureBufferSize, kTimeout, true);
IRsend irsend(kSendIRLed);
WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

//   PROTÓTIPOS DAS FUNÇÕES DEFINIDAS EM <holhooja.h>
void setup_wifi(const char *ssid, const char *password);
void connect_MQTT(IPAddress mqtt_server, int mqtt_port, PubSubClient *mqttClient);
void IRAM_ATTR detectsMovement();
void ler_Movimento(int MovementTimer, int led);
void ler_SinalIR(IRrecv *irrecv);
void ler_DHT(DHTStable *DHT, PubSubClient *mqttClient, int DHT11_PIN, int DHTReadTimer);
void ler_ldr(int LDR_PIN, PubSubClient *mqttClient, int LDRReadTimer);
void verificarConexao(PubSubClient *mqttClient);
void ler_sct(int sctPin, EnergyMonitor *emon1, int SCTReadTimer, PubSubClient *mqttClient);

//void ler_sct();

void callback(char *topic, byte *message, unsigned int length) {
  Serial.print("Mensagem entregue no tópico: ");
  Serial.print(topic);
  Serial.print("] ");
  Serial.print(". Message: ");
  String messageTemp;

  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

  if (String(topic) == topicEspAr) {
    Serial.println("Comandos: ");

    if (messageTemp == "on") {
      Serial.println("on");
      enviar_SinalIR(&irsend, 1);
      //neopixelWrite(RGB_BUILTIN,RGB_BRIGHTNESS,RGB_BRIGHTNESS,RGB_BRIGHTNESS);
    } else if (messageTemp == "off") {
      Serial.println("off");
      enviar_SinalIR(&irsend, 0);
      //neopixelWrite(RGB_BUILTIN,0,0,0);
    } else if (messageTemp == "up") {
      Serial.println("up");
      neopixelWrite(RGB_BUILTIN, 0, 0, RGB_BRIGHTNESS);  // Blue
    } else if (messageTemp == "down") {
      Serial.println("down");
      neopixelWrite(RGB_BUILTIN, RGB_BRIGHTNESS, RGB_BRIGHTNESS, 0);  // Yellow
    } else if (messageTemp == "left") {
      Serial.println("left");
      neopixelWrite(RGB_BUILTIN, RGB_BRIGHTNESS, 0, 0);
    } else if (messageTemp == "right") {
      Serial.println("right");
      neopixelWrite(RGB_BUILTIN, RGB_BRIGHTNESS, 0, RGB_BRIGHTNESS);
    }

  }

  if (String(topic) == topicEspPorta) {
    if (messageTemp == "porta") {
      digitalWrite(RelePin, LOW); //aciona o pino
      delay(100);
      digitalWrite(RelePin, HIGH); //aciona o pino
      delay(100);
      enviar_SinalIR(&irsend, 1);

    }

  }

  if (String(topic) == topicEspLED) {
    Serial.println("LED");
  }
}

//   FUNÇÃO DE CONFIGURAÇÃO
void setup() {
  Serial.begin(115200);                 // Inicia a comunicação serial
  pinMode(motionSensor, INPUT_PULLUP);  // PIR Motion Sensor mode INPUT_PULLUP
  // MQ135 SENSOR GPIO
  pinMode(MQ135_D_PIN, INPUT);
  attachInterrupt(digitalPinToInterrupt(motionSensor), detectsMovement, RISING);  // Defini uma interrupção em caso de leitura do sensor de movimento
  pinMode(led, OUTPUT);
  digitalWrite(led, LOW);                             // LED DE TESTE
  pinMode(kRecvPin, INPUT);                           // Configurar o pino do receptor IR
  irrecv.enableIRIn();                                // Inicia o receptor IR
  irsend.begin();                                     // Inicia o emissor IR
  setup_wifi(ssid, password);                         // Inicia conexão wifi
  connect_MQTT(mqtt_server, mqtt_port, &mqttClient);  // Estabelece conexão com o Broker MQTT e faz o SUBSCRIBE dos tópicos
  verificarConexao(&mqttClient);
  mqttClient.setCallback(callback);
  //Sensor de Corrente
  emon1.current(sctPin, 111.1);             // Current: input pin, calibration.
  pinMode(RelePin, OUTPUT); // seta o pino como saída
  digitalWrite(RelePin, HIGH);

}

void loop() {
  mqttClient.loop();                               // Mantem a conexão com o broker
  ler_SinalIR(&irrecv);                            // Verificar se um sinal IR foi recebido
  ler_Movimento(MovementTimer, led, &mqttClient);  // Aguarda timeSeconds para registrar um novo acionamento e no caso de movimento o led liga
  ler_DHT(&DHT, &mqttClient, DHT11_PIN, DHTReadTimer);
//  ler_ldr(LDR_PIN, &mqttClient, LDRReadTimer);
  ler_mq135(&mqttClient, MQ135_D_PIN, MQ135_A_PIN, MQ135ReadTimer);
  ler_sct(sctPin, &emon1, SCTReadTimer, &mqttClient);
 
  delay(500);
}

