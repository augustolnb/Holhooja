#include <IRrecv.h>
#include <WiFi.h>
#include <PubSubClient.h>

boolean startTimer = false;
int i;
unsigned long lastSensorRead;

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
  lastSensorRead = millis();
}

void ler_Movimento(int MovementTimer, int led){
  unsigned long currentMillis = millis();
  boolean motion = false;

  if((digitalRead(led) == HIGH) && (motion == false)) {
    //Serial.println("MOVIMENTO DETECTADO!!!");
    motion = true;
  //    enviar_SinalIR();
  }
  // Turn off the LED after the number of seconds defined in the timeSeconds variable
  if(startTimer && (currentMillis - lastSensorRead > MovementTimer)) {
    Serial.println("Sem movimento...");
    digitalWrite(led, LOW);
    startTimer = false;
    motion = false;
  }
}
/*
void ler_DHT(DHTStable *DHT, int DHT11_PIN, int DHTReadTimer) {
  int chk = DHT->read11(DHT11_PIN);
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
  // DISPLAY DATA
  unsigned long currentMillis = millis();
  if (currentMillis - lastSensorRead >= DHTReadTimer) {
    Serial.print(DHT->getHumidity(), 1);
    Serial.print(",\t");
    Serial.println(DHT->getTemperature(), 1);
    lastSensorRead = currentMillis;
  }
}
*/

void ler_DHT(DHTStable *DHT, PubSubClient *mqttClient, int DHT11_PIN, int DHTReadTimer) {
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
  
  if (currentMillis - lastSensorRead >= DHTReadTimer) {
    humidity = DHT->getHumidity();
    temperature = DHT->getTemperature();

    if (isnan(humidity) || isnan(temperature)) {
      humidity = 0.0;
      temperature = 0.0;
    }

    Serial.printf("Umidade: %.1f%%, Temperatura: %.1f°C \n", humidity, temperature);

    lastSensorRead = currentMillis;

    // Create JSON string for MQTT publication
    char jsonBuffer[128];
    snprintf(jsonBuffer, 128, "{'Umidade' : %.1f, 'Temperatura' : %.1f}", humidity,  temperature);

    // Publish sensor data to MQTT topic
    mqttClient->publish("topicoDHT", jsonBuffer);
  }
}

void callback(char* topic, byte* payload, unsigned int length){
    Serial.print("Mensagem entregue [");
    Serial.print(topic);
    Serial.print("] ");
/*
    for(int i=0;i<length;i++){
      Serial.print((char)payload[i]);
    }
    Serial.println("");

    if((char)payload[0] == '1'){
      digitalWrite(20, LOW);
    }
    else{
      digitalWrite(20, HIGH);
    }
*/
}

void connect_MQTT(IPAddress mqtt_server, int mqtt_port, PubSubClient *mqttClient, const char *topicoDHT){
  mqttClient->setKeepAlive( 90 );
  mqttClient->setServer(mqtt_server, mqtt_port);

  while (!mqttClient->connected()) {
    if (mqttClient->connect("ESP32-S3")) {
      mqttClient->subscribe(topicoDHT); 
      // mqttClient->subscribe(topicoMov); 
      // mqttClient->subscribe(topico); 

      Serial.println("MQTT Conectado > ESP32-S3");
      Serial.print("\nInscrito no tópico:");
      // imprime o nome do tópico inscrito
      int i = 0;
      while (topicoDHT[i] != '\0') {
        Serial.print(topicoDHT[i]);
        i++;
      }
      Serial.println();
      delay(500);
    } else {
      Serial.println("MQTT connect fail");
      delay(3000);
    }
  }
  mqttClient->setCallback( callback );
}

