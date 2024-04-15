#include "DHTStable.h"
#include "holhooja.h"
#include <Arduino.h>
#include <IRrecv.h>
#include <IRutils.h>
#include <IRsend.h>

//
//  DEFINIÇÃO DAS CONSTANTES
//

//#define DHT11_PIN       21
#define pushButton_pin  15

const int timeSeconds = 4;
const int DHT11_PIN = 21;
const int DHTReadTimer = 10000; // miliseconds
const int led = 20;
const int kRecvPin = 47;
const uint8_t kTimeout = 50;
const int motionSensor = 19;
const uint16_t kSendIRLed = 48;
const uint16_t kCaptureBufferSize = 1024;
//
//  INICIALIZAÇÃO DAS VARIÁVEIS
//


uint16_t rawData[199] = {4356, 4418,  516, 1650,  490, 606,  488, 1652,  514, 1652,  514, 556,  488, 606,  490, 1652,  490, 606,  488, 580,  490, 1676,  490, 580,  490, 608,  488, 1650,  490, 1678,  490, 580,  514, 1654,  488, 580,  514, 1652,  490, 1652,  488, 1678,  490, 1676,  514, 556,  490, 1676,  514, 1628,  512, 1654,  488, 582,  490, 606,  514, 556,  490, 606,  490, 1652,  490, 606,  514, 556,  490, 1676,  514, 1626,  488, 1678,  514, 556,  514, 582,  514, 556,  488, 606,  490, 580,  490, 606,  490, 580,  514, 556,  540, 1626,  514, 1652,  514, 1628,  514, 1652,  514, 1626,  514, 5204,  4354, 4418,  518, 1650,  514, 582,  514, 1626,  512, 1654,  514, 556,  514, 582,  514, 1626,  514, 582,  514, 554,  490, 1676,  514, 554,  514, 582,  514, 1626,  514, 1652,  514, 554,  514, 1652,  514, 556,  540, 1628,  512, 1652,  514, 1626,  514, 1654,  490, 580,  514, 1650,  490, 1650,  490, 1676,  490, 606,  490, 580,  490, 580,  490, 606,  490, 1650,  492, 604,  490, 580,  490, 1676,  490, 1676,  492, 1650,  490, 606,  492, 578,  490, 580,  490, 606,  490, 580,  490, 606,  490, 580,  490, 604,  490, 1652,  490, 1676,  490, 1650,  490, 1676,  490, 1676,  490};  // COOLIX B27BE0

//
// CRIAÇÃO DOS OBJETOS DE CADA CLASSE
//

DHTStable DHT;
IRrecv irrecv(kRecvPin, kCaptureBufferSize,  kTimeout, true);
IRsend irsend(kSendIRLed); 

//
//   PROTÓTIPOS DAS FUNÇÕES
//

void ler_SinalIR(IRrecv *irrecv);
void IRAM_ATTR detectsMovement();
void ler_Movimento(int timeSeconds, int led);
void ler_DHT(DHTStable *DHT, int DHT11_PIN, int DHTReadTimer);

void setup() {
  // Iniciar comunicação serial
  Serial.begin(115200);
  // PIR Motion Sensor mode INPUT_PULLUP
  pinMode(motionSensor, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(motionSensor), detectsMovement, RISING);
  // LED DE TESTE
  pinMode(led, OUTPUT);
  digitalWrite(led, LOW);
  // Configurar o pino do receptor IR
  pinMode(kRecvPin, INPUT);
  // Inicia o receptor IR
  irrecv.enableIRIn();
  // Inicia o emissor IR
  irsend.begin();
}

void loop() {
  // Verificar se um sinal IR foi recebido
  ler_SinalIR(&irrecv, led);

  ler_Movimento(timeSeconds, led);

  ler_DHT(&DHT, DHT11_PIN, DHTReadTimer);
  
}







