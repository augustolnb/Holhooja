#include <IRrecv.h>
#include <WiFi.h>
#include <PubSubClient.h>

boolean startTimer = false;
int i;
unsigned long lastDhtRead;
unsigned long lastLdrRead;
unsigned long lastSrRead;
const char* topicEspAr = "/comandos/esp32/ar"; // subscribe
const char* topicEspPorta = "/comandos/esp32/porta"; // subscribe
const char* topicEspLED = "/comandos/esp32/led"; // subscribe
const char* topicSensorDHT = "/sensores/DHT"; // publish
const char* topicSensorLDR = "/sensores/LDR"; // publish
const char* topicSensorSR602 = "/sensores/SR602"; // publish

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

/*
void enviar_SinalIR(){
  irsend.sendRaw(rawData, 199, 38);  // Send a raw data capture at 38kHz.
  Serial.println("Código enviado");
  delay(100);
}
*/

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


void callback(char* topic, byte* message, unsigned int length){
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

    if(messageTemp == "on"){
      Serial.println("on");
      neopixelWrite(RGB_BUILTIN,RGB_BRIGHTNESS,0,0);
    }
    else if(messageTemp == "off"){
      Serial.println("off");
      neopixelWrite(RGB_BUILTIN,RGB_BRIGHTNESS,0,RGB_BRIGHTNESS); 
    }
  } 
  if (String(topic) == topicEspPorta) {
    Serial.println("PORTA");
    //controle_IR(messageTemp, "porta");
  } 
  if (String(topic) == topicEspLED) {
    Serial.println("LED");
    
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
      
      Serial.print("\nInscrito nos tópicos:");
      Serial.println(topicEspAr);
      Serial.println(topicEspPorta);
      delay(500);
    } else {
      Serial.println("MQTT connect fail");
      delay(3000);
    }
  }
  mqttClient->setCallback( callback );
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



/*
  IMPLEMENTAR FUNÇÃO QUE FAÇA O A LEITURA DO BROKER MQTT
  ESSA FUNÇÃO
*/
