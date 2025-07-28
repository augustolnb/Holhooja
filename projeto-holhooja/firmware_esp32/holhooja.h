#include <IRrecv.h>
#include <IRsend.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include "EmonLib.h"

uint16_t ligar_17[199] = {4376, 4388,  542, 1624,  514, 554,  542, 1624,  514, 1650,  516, 526,  542, 552,  544, 1622,  514, 552,  544, 526,  540, 1650,  516, 526,  540, 554,  542, 1624,  514, 1652,  514, 526,  544, 1650,  516, 524,  544, 554,  540, 1624,  516, 1650,  514, 1650,  514, 1624,  514, 1650,  516, 1624,  514, 1650,  516, 1624,  516, 552,  544, 526,  540, 554,  542, 526,  544, 552,  542, 526,  544, 550,  544, 526,  542, 528,  566, 528,  542, 526,  544, 552,  542, 526,  542, 552,  544, 1624,  516, 1650,  514, 1622,  542, 1624,  516, 1648,  516, 1622,  516, 1648,  514, 1624,  516, 5198,  4378, 4388,  542, 1624,  516, 552,  542, 1622,  516, 1650,  514, 526,  544, 550,  544, 1624,  514, 554,  542, 526,  542, 1650,  516, 526,  542, 552,  544, 1622,  516, 1648,  516, 526,  542, 1648,  516, 524,  572, 526,  542, 1650,  516, 1622,  514, 1650,  514, 1624,  514, 1652,  514, 1622,  516, 1648,  516, 1650,  516, 526,  542, 554,  542, 526,  542, 528,  544, 550,  542, 526,  542, 552,  544, 526,  542, 552,  542, 528,  542, 552,  544, 524,  544, 528,  542, 552,  542, 1650,  514, 1624,  516, 1650,  516, 1624,  516, 1648,  516, 1622,  516, 1648,  516, 1650,  516};
uint16_t ligar_20[199] = {4376, 4388,  542, 1624,  514, 552,  544, 1622,  518, 1648,  516, 526,  544, 552,  542, 1624,  516, 552,  544, 524,  544, 1648,  514, 528,  542, 552,  544, 1624,  514, 1650,  516, 526,  542, 1648,  516, 526,  544, 552,  542, 1622,  516, 1650,  516, 1650,  514, 1624,  516, 1650,  514, 1622,  516, 1652,  512, 1624,  516, 552,  544, 524,  544, 554,  542, 528,  542, 550,  544, 526,  544, 550,  544, 526,  542, 1648,  516, 526,  542, 552,  544, 524,  544, 526,  544, 550,  544, 1624,  514, 1650,  514, 528,  568, 1624,  516, 1650,  516, 1622,  516, 1648,  516, 1622,  516, 5196,  4378, 4388,  544, 1624,  514, 552,  544, 1622,  514, 1650,  516, 526,  542, 554,  542, 1624,  516, 552,  544, 526,  544, 1648,  516, 526,  542, 552,  542, 1624,  516, 1648,  516, 528,  542, 1648,  516, 526,  568, 526,  544, 1648,  516, 1624,  514, 1650,  516, 1624,  514, 1648,  516, 1624,  514, 1648,  516, 1650,  516, 526,  542, 554,  542, 526,  542, 526,  544, 552,  542, 526,  542, 554,  542, 526,  542, 1648,  516, 528,  542, 552,  542, 528,  540, 554,  540, 526,  544, 1650,  514, 1622,  516, 554,  542, 1620,  514, 1650,  514, 1622,  516, 1648,  516, 1648,  518};  // COOLIX B23F20
uint16_t desligar[199] = {4376, 4388,  544, 1622,  514, 554,  542, 1622,  516, 1650,  514, 528,  544, 552,  540, 1622,  518, 552,  542, 526,  544, 1650,  514, 526,  544, 552,  544, 1622,  514, 1650,  516, 526,  542, 1648,  516, 528,  540, 1650,  516, 1622,  516, 1648,  516, 1648,  518, 524,  544, 1648,  516, 1622,  516, 1648,  516, 526,  542, 554,  542, 526,  540, 554,  542, 1622,  516, 552,  542, 528,  542, 1650,  516, 1622,  516, 1650,  514, 526,  544, 552,  542, 526,  542, 552,  542, 526,  542, 552,  542, 526,  542, 526,  570, 1622,  516, 1648,  516, 1624,  516, 1650,  516, 1622,  516, 5196,  4378, 4388,  544, 1622,  514, 554,  542, 1622,  516, 1650,  516, 528,  542, 552,  544, 1624,  516, 550,  542, 526,  542, 1648,  518, 524,  542, 556,  540, 1624,  514, 1648,  516, 524,  544, 1648,  516, 526,  568, 1622,  516, 1648,  518, 1622,  516, 1650,  516, 526,  544, 1648,  516, 1622,  516, 1648,  516, 552,  542, 526,  544, 528,  540, 554,  542, 1622,  516, 552,  542, 524,  544, 1650,  516, 1650,  516, 1622,  516, 552,  544, 526,  544, 526,  542, 552,  544, 526,  542, 552,  544, 526,  544, 552,  542, 1622,  516, 1650,  516, 1624,  516, 1648,  516, 1648,  516};  // COOLIX B27BE0

boolean startTimer = false;
int i;
unsigned long lastMq135Read;
unsigned long lastSctRead;
unsigned long lastDhtRead;
unsigned long lastLdrRead;
unsigned long lastSrRead;

// Tópicos MQTT
const char* topicEspAr = "/comando/esp32/AC"; // subscribe
const char* topicEspPorta = "/comandos/esp32/porta"; // subscribe
const char* topicEspLED = "/comando/esp32/lampada"; // subscribe
const char* topicSensorDHT = "/sensores/DHT"; // publish
const char* topicSensorLDR = "/sensores/LDR"; // publish
const char* topicSensorSR602 = "/sensores/SR602"; // publish
const char* topicSensorSCT = "/sensores/SCT"; // publish
const char* topicSensorMQ135 = "/sensores/MQ135"; // publish

void setup_wifi(const char *ssid, const char *password){
  delay(10);
  Serial.println("");
  Serial.print("Conectando a rede");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while(WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");
    }

    randomSeed(micros());

    Serial.println("");
    Serial.println("WiFi conectado");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
}

void enviar_SinalIR(IRsend *irsend, int comando){  // 1->liga 17ºc   2->ligar 20ºc 0->desliga
  Serial.println(comando);
  if(comando == 0)
    irsend->sendRaw(desligar, 199, 38);  // Send a raw data capture at 38kHz.
  
  if(comando == 1)
    irsend->sendRaw(ligar_17, 199, 38);  // Send a raw data capture at 38kHz.
    
  if(comando == 2)
    irsend->sendRaw(ligar_20, 199, 38);  // Send a raw data capture at 38kHz.
  
  Serial.println("Código enviado");
  delay(100);
}

void ler_SinalIR(IRrecv *irrecv){
  decode_results results;
  if (irrecv->decode(&results)) {
    unsigned long hex = results.value;

    //    Serial.println(resultToHumanReadableBasic(&results));
    /*
    if(hex == 0x1FFF807){
      for(i=0;i<10;i++){
        digitalWrite(ledIR, HIGH);
        delay(100);
        digitalWrite(ledIR, LOW);
        delay(100);
      }
    }
    */
    if(hex == 0x1FFC03F){
      #ifdef RGB_BUILTIN
        Serial.println("Botão esquerdista: altera led vermelho");
        neopixelWrite(RGB_BUILTIN,RGB_BRIGHTNESS,0,0); // Red
      #endif
    }
    
    if(hex == 0x1FF40BF){
      #ifdef RGB_BUILTIN
         Serial.println("Botão direto: altera led azul");
        neopixelWrite(RGB_BUILTIN,0,0,RGB_BRIGHTNESS); // Blue
      #endif
    }

    if(hex == 0x1FF807F){
      #ifdef RGB_BUILTIN
         Serial.println("Botão p/ baixo: led roxo");
        neopixelWrite(RGB_BUILTIN,RGB_BRIGHTNESS,0,RGB_BRIGHTNESS); // Purple
      #endif
    }

    if(hex == 0x1FF00FF){
      #ifdef RGB_BUILTIN
         Serial.println("Botão p/ cima: led amarelo");
        neopixelWrite(RGB_BUILTIN,RGB_BRIGHTNESS,RGB_BRIGHTNESS,0); // Yellow
      #endif
    }
 
    irrecv->resume();
  }
  delay(100);
}

void IRAM_ATTR detectsMovement() {
  int led = 20;
  digitalWrite(led, HIGH);
  startTimer = true;
  lastSrRead = millis();
}

void ler_Movimento(int MovementTimer, int led, PubSubClient *mqttClient){
  unsigned long currentMillis = millis();
  boolean motion = false;

  if((digitalRead(led) == HIGH) && (motion == false)) {
    motion = true;
    char jsonBuffer[128];
    snprintf(jsonBuffer, 128, "{'Movimento' : 1, }");
    mqttClient->publish(topicSensorSR602, jsonBuffer);
  //    enviar_SinalIR();
  }
  if(startTimer && (currentMillis - lastSrRead > MovementTimer)) {
    Serial.println("Sem movimento...");
    digitalWrite(led, LOW);
    startTimer = false;
    motion = false;
    char jsonBuffer[128];
    snprintf(jsonBuffer, 128, "{'Movimento' : 0, }");
    mqttClient->publish(topicSensorSR602, jsonBuffer);
  }
}

void ler_DHT(DHTStable *DHT, PubSubClient *mqttClient, int DHT11_PIN, int DHTReadTimer) {
  // variaveis para leitura do DHT11
  int chk = DHT->read11(DHT11_PIN);
  unsigned long currentMillis = millis();
  float humidity=0.0;
  float temperature=0.0;

  switch (chk)
  {
    case DHTLIB_OK:  
      //Serial.print("OK,\t"); 
      break;
    case DHTLIB_ERROR_CHECKSUM: 
      Serial.print("Checksum error,\t"); 
      break;
    case DHTLIB_ERROR_TIMEOUT: 
      Serial.print("Time out error,\t"); 
      break;
    default: 
      Serial.print("Unknown error,\t"); 
      break;
  }
  
  if (currentMillis - lastDhtRead >= DHTReadTimer) {
    humidity = DHT->getHumidity();
    temperature = DHT->getTemperature();

    if (isnan(humidity) || isnan(temperature)) {
      humidity = 0.0;
      temperature = 0.0;
    }

    Serial.printf("Umidade: %.1f%%, Temperatura: %.1f°C \n", humidity, temperature);

    lastDhtRead = currentMillis;

    // Create JSON string for MQTT publication
    char jsonBuffer[128];
    snprintf(jsonBuffer, 128, "{'Umidade' : %.1f, 'Temperatura' : %.1f}", humidity,  temperature);

    // Publish sensor data to MQTT topic
    mqttClient->publish(topicSensorDHT, jsonBuffer);
  }
}


void ler_mq135(PubSubClient *mqttClient, int MQ135_D_PIN, int MQ135_A_PIN, int MQ135ReadTimer) {
  unsigned long currentMillis = millis();
  float presenca=0.0;
  float quantidade=0.0;

  if (currentMillis - lastMq135Read >= MQ135ReadTimer) {
    presenca = digitalRead(MQ135_D_PIN);
    ////////////////////////////////////////////////////////////////  
    if (presenca == HIGH)
      Serial.println("Sem gases nocivos detectados.");
    else
      Serial.println("Gases nocivos detectados!");
    ////////////////////////////////////////////////////////////////  
    quantidade = analogRead(MQ135_A_PIN);
    Serial.print("Quantidade de gás detectada: ");
    Serial.println(quantidade);
    ////////////////////////////////////////////////////////////////

    if (isnan(presenca) || isnan(quantidade)) {
      presenca = 0.0;
      quantidade = 0.0;
    }

    //Serial.printf("presenca: %.1f, quantidade: %.1f \n", presenca, quantidade);

    lastMq135Read = currentMillis;

    // Create JSON string for MQTT publication
    char jsonBuffer[128];
    snprintf(jsonBuffer, 128, "{'presenca' : %.1f, 'quantidade' : %.1f}", presenca,  quantidade);

    if(quantidade > 200){
       for(i=0;i<10;i++){
        #ifdef RGB_BUILTIN
            neopixelWrite(RGB_BUILTIN,RGB_BRIGHTNESS,0,0); // Red
            delay(500);
            neopixelWrite(RGB_BUILTIN,0,0,0); // off
            delay(500);
          #endif
        }
    }

    // Publish sensor data to MQTT topic
    mqttClient->publish(topicSensorMQ135, jsonBuffer);
  }
}

void connect_MQTT(IPAddress mqtt_server, int mqtt_port, PubSubClient *mqttClient){
  mqttClient->setKeepAlive( 90 );
  mqttClient->setServer(mqtt_server, mqtt_port);

  while (!mqttClient->connected()) {
    if (mqttClient->connect("ESP32-S3")) {
      Serial.println("inscrição aqui");
      mqttClient->subscribe(topicEspAr); 
      mqttClient->subscribe(topicEspPorta); 

      Serial.println("MQTT Conectado > ESP32-S3");
      
      Serial.println("\nInscrito nos tópicos:");
      Serial.println(topicEspAr);
      Serial.println(topicEspPorta);
      delay(500);
    } else {
      Serial.println("MQTT connect fail");
      delay(3000);
    }
  }
}


void ler_sct(int sctPin, EnergyMonitor *emon1, int SCTReadTimer, PubSubClient *mqttClient){
  unsigned long currentMillis = millis();
  float lastSCTRead=0;

  if (currentMillis - lastSCTRead >= SCTReadTimer) {
    double Irms = emon1->calcIrms(1480);  // Calculate Irms only
    if (isnan(Irms)) {
      Irms = 0.0;
    }
    /*
    if (Irms < 4) {
      Serial.printf("Status: Desligado \n");
      lastSCTRead = currentMillis;
    }

    if (Irms > 4) {
      Serial.printf("Status: Ligado \n");
      lastSCTRead = currentMillis;
    }
    */

    lastSCTRead = currentMillis; // Create JSON string for MQTT publication
    
    char jsonBuffer[128];
    snprintf(jsonBuffer, 128, "{'Status_AC' : %.1f}", Irms);

    // Publish sensor data to MQTT topic
    mqttClient->publish(topicSensorSCT, jsonBuffer);
  }
}

void ler_ldr(int LDR_PIN, PubSubClient *mqttClient, int LDRReadTimer){
  unsigned long currentMillis = millis();

  if (currentMillis - lastLdrRead >= LDRReadTimer) {
    int ldr_value = analogRead(LDR_PIN);
    if (isnan(ldr_value)) {
      ldr_value = 0.0;
    }
    Serial.printf("Luminosidade: %d \n", ldr_value);
    lastLdrRead = currentMillis;

    char jsonBuffer[128];
    snprintf(jsonBuffer, 128, "{'Luminosidade' : %d, }", ldr_value);
    mqttClient->publish(topicSensorLDR, jsonBuffer);
  }
}

void verificarConexao(PubSubClient *mqttClient){
  
  mqttClient->subscribe("/esp32/verificarConexao");
  mqttClient->subscribe("/esp32/enviarComando");
  
  printf("Inscrito no tópico: '/esp32/verificarConexao'\n");
  printf("Inscrito no tópico: '/esp32/enviarComando'\n");

}


