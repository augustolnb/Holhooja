#include <IRrecv.h>

unsigned long lastTrigger = 0;
boolean startTimer = false;
int i;
unsigned long lastSensorRead;

/*
void enviar_SinalIR(){
  irsend.sendRaw(rawData, 199, 38);  // Send a raw data capture at 38kHz.
  Serial.println("Código enviado");
  delay(100);
}
*/

void ler_SinalIR(IRrecv *irrecv, int led){
  decode_results results;
  if (irrecv->decode(&results)) {
    unsigned long hex = results.value;

    //    Serial.println(resultToHumanReadableBasic(&results));

    if(hex == 0x1FFF807){
      for(i=0;i<10;i++){
        digitalWrite(led, HIGH);
        delay(100);
        digitalWrite(led, LOW);
        delay(100);
      }
    }
    
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
  lastTrigger = millis();
}

void ler_Movimento(int timeSeconds, int led){
  unsigned long now = millis();
  boolean motion = false;

  now = millis();
  if((digitalRead(led) == HIGH) && (motion == false)) {
    //Serial.println("MOVIMENTO DETECTADO!!!");
    motion = true;
  //    enviar_SinalIR();
  }
  // Turn off the LED after the number of seconds defined in the timeSeconds variable
  if(startTimer && (now - lastTrigger > (timeSeconds*1000))) {
    Serial.println("Sem movimento...");
    digitalWrite(led, LOW);
    startTimer = false;
    motion = false;
  }
}

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