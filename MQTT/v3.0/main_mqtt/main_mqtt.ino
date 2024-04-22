#include <WiFi.h>
#include <PubSubClient.h>
#include "DHTStable.h"

const int DHT11_PIN = 21;
const int DHTReadTimer = 10000;
const int mqtt_port = 1883;
const char* ssid = "Bomba atomica 2G";
const char* password = "microondas";

IPAddress mqtt_server(192, 168, 100, 168);

DHTStable DHT;
WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);

struct SensorData {
  float humidity;
  float temperature;
};

void setup_wifi(){
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
    Serial.println("IP: ");
    Serial.println(WiFi.localIP());
}

SensorData ler_DHT(DHTStable *DHT, int DHT11_PIN, int DHTReadTimer) {
  int chk = DHT->read11(DHT11_PIN);
  unsigned long lastSensorRead;
  unsigned long currentMillis = millis();
  float humidity=0.0;
  float temperature=0.0;

  SensorData DHTdata = {humidity, temperature};
  
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
  if (currentMillis - lastSensorRead >= DHTReadTimer) {
    humidity = DHT->getHumidity();
    temperature = DHT->getTemperature();

    if (isnan(humidity) || isnan(temperature)) {
      humidity = 0.0;
      temperature = 0.0;
    }
    lastSensorRead = currentMillis;
    DHTdata = {humidity, temperature};
  }
  return DHTdata;
}

void callback(char* topic, byte* payload, unsigned int length){
    Serial.print("Mensagem entregue [");
    Serial.print(topic);
    Serial.print("] ");

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
}

/* EXEMPLO
void mqtt_data(char* topic, byte* msg, unsigned int t_size) {
  // Implement message handling logic here (if needed)
}
*/

void connect_MQTT(){
  mqtt.setKeepAlive( 90 );
  mqtt.setServer(mqtt_server, mqtt_port);

  while (!mqtt.connected()) {
    if (mqtt.connect("ESP32-S3")) {
      Serial.println("MQTT Conectado");
      mqtt.subscribe("temp"); 
      Serial.println("Inscrito no tópico: temp");
      delay(500);
    } else {
      Serial.println("MQTT connect fail");
      delay(3000);
    }
  }
  mqtt.setCallback( callback );
  mqtt.subscribe("temp");
}

void setup() {
  pinMode(20, OUTPUT);    
  
  Serial.begin(115200);
  
  setup_wifi();

  connect_MQTT();
}

void loop() {
  mqtt.loop(); // Process MQTT messages and maintain connection

  SensorData readings = ler_DHT(&DHT, DHT11_PIN, DHTReadTimer);

  // Format and print sensor data to serial
  Serial.printf("Umidade: %.1f%%, Temperatura: %.1f°C \n", readings.humidity, readings.temperature);

  // Create JSON string for MQTT publication
  char jsonBuffer[128];
  snprintf(jsonBuffer, 128, "{'Umidade' : %.1f, 'Temperatura' : %.1f}", readings.humidity,  readings.temperature);

  // Publish sensor data to MQTT topic
  mqtt.publish("temp", jsonBuffer);

  delay(2000); // Add a delay between MQTT publications (adjust as needed)
}
