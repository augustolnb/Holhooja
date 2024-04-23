#include "DHTStable.h"
#include "holhooja.h"
#include <Arduino.h>
#include <IRrecv.h>
#include <IRutils.h>
#include <IRsend.h>
#include <WiFi.h>
#include <PubSubClient.h>

//
//  DEFINIÇÃO DAS CONSTANTES
//
const int MovementTimer = 4000; // 4s
const int DHT11_PIN = 21;
const int DHTReadTimer = 10000; // 10s
const int led = 20;
const int kRecvPin = 47;
const uint8_t kTimeout = 50;
const int motionSensor = 19;
const uint16_t kSendIRLed = 48;
const uint16_t kCaptureBufferSize = 1024;

// CONSTANTES DE CONEXÃO MQTT
IPAddress mqtt_server(192, 168, 100, 168);
const int mqtt_port = 1883;
const char* topicoDHT = "topicoDHT";

// CONSTANTES DE CONEXÃO WIFI
const char* ssid = "Bomba atomica 2G";
const char* password = "microondas";

//  DEFINIÇÃO DAS VARIÁVEIS DE COMANDOS IR
uint16_t rawData[199] = {4356, 4418,  516, 1650,  490, 606,  488, 1652,  514, 1652,  514, 556,  488, 606,  490, 1652,  490, 606,  488, 580,  490, 1676,  490, 580,  490, 608,  488, 1650,  490, 1678,  490, 580,  514, 1654,  488, 580,  514, 1652,  490, 1652,  488, 1678,  490, 1676,  514, 556,  490, 1676,  514, 1628,  512, 1654,  488, 582,  490, 606,  514, 556,  490, 606,  490, 1652,  490, 606,  514, 556,  490, 1676,  514, 1626,  488, 1678,  514, 556,  514, 582,  514, 556,  488, 606,  490, 580,  490, 606,  490, 580,  514, 556,  540, 1626,  514, 1652,  514, 1628,  514, 1652,  514, 1626,  514, 5204,  4354, 4418,  518, 1650,  514, 582,  514, 1626,  512, 1654,  514, 556,  514, 582,  514, 1626,  514, 582,  514, 554,  490, 1676,  514, 554,  514, 582,  514, 1626,  514, 1652,  514, 554,  514, 1652,  514, 556,  540, 1628,  512, 1652,  514, 1626,  514, 1654,  490, 580,  514, 1650,  490, 1650,  490, 1676,  490, 606,  490, 580,  490, 580,  490, 606,  490, 1650,  492, 604,  490, 580,  490, 1676,  490, 1676,  492, 1650,  490, 606,  492, 578,  490, 580,  490, 606,  490, 580,  490, 606,  490, 580,  490, 604,  490, 1652,  490, 1676,  490, 1650,  490, 1676,  490, 1676,  490};  // COOLIX B27BE0

//
// CRIAÇÃO DOS OBJETOS DE CADA CLASSE
//
DHTStable DHT;
IRrecv irrecv(kRecvPin, kCaptureBufferSize,  kTimeout, true);
IRsend irsend(kSendIRLed); 
WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

//
//   PROTÓTIPOS DAS FUNÇÕES DEFINIDAS EM <holhooja.h>
//
void setup_wifi(const char *ssid,const char *password);
void ler_SinalIR(IRrecv *irrecv);
void IRAM_ATTR detectsMovement();
void ler_Movimento(int MovementTimer, int led);
void ler_DHT(DHTStable *DHT, PubSubClient *mqttClient, int DHT11_PIN, int DHTReadTimer);
void connect_MQTT(IPAddress mqtt_server, int mqtt_port, PubSubClient *mqttClient, const char *topicoDHT);

//
//   FUNÇÃO DE CONFIGURAÇÃO
//
void setup() {
  Serial.begin(115200); // Inicia a comunicação serial
  pinMode(motionSensor, INPUT_PULLUP); // PIR Motion Sensor mode INPUT_PULLUP
  attachInterrupt(digitalPinToInterrupt(motionSensor), detectsMovement, RISING); // Defini uma interrupção em caso de leitura do sensor de movimento
  pinMode(led, OUTPUT); digitalWrite(led, LOW); // LED DE TESTE
  pinMode(kRecvPin, INPUT); // Configurar o pino do receptor IR
  irrecv.enableIRIn(); // Inicia o receptor IR
  irsend.begin(); // Inicia o emissor IR
  setup_wifi(ssid, password); // Inicia conexão wifi
  connect_MQTT(mqtt_server, mqtt_port, &mqttClient, topicoDHT); // Estabelece conexão com o Broker MQTT e faz o SUBSCRIBE dos tópicos
}

void loop() {
  mqttClient.loop(); // Mantem a conexão com o broker

  ler_SinalIR(&irrecv); // Verificar se um sinal IR foi recebido

  ler_Movimento(MovementTimer, led); // Aguarda timeSeconds para registrar um novo acionamento e no caso de movimento o led liga

  ler_DHT(&DHT, &mqttClient, DHT11_PIN, DHTReadTimer);

}




