/*
const int led = 15;
const int motionSensor = 20; 

void setup(){
  pinMode(motionSensor,INPUT);
  pinMode(led,OUTPUT);
  Serial.begin(9600);

  attachInterrupt();
}

void loop(){
  bool motion=digitalRead(motionSensor);
  Serial.println(motion);
  delay(1000);
}
*/



/*
#define pushButton_pin   15
#define LED_pin   20
 
void IRAM_ATTR toggleLED()
{
  digitalWrite(LED_pin, !digitalRead(LED_pin));
}
 
void setup()
{
  pinMode(LED_pin, OUTPUT);
  pinMode(pushButton_pin, INPUT);
  attachInterrupt(pushButton_pin, toggleLED, RISING);
}
 
void loop()
{
}
*/


/*

#define timeSeconds 4

// Set GPIOs for LED and PIR Motion Sensor
const int led = 20;
const int motionSensor = 19;

// Timer: Auxiliary variables
unsigned long now = millis();
unsigned long lastTrigger = 0;
boolean startTimer = false;
boolean motion = false;

// Checks if motion was detected, sets LED HIGH and starts a timer
void IRAM_ATTR detectsMovement() {
  digitalWrite(led, HIGH);
  startTimer = true;
  lastTrigger = millis();
}

void setup() {
  // Serial port for debugging purposes
  Serial.begin(9600);

  
  // PIR Motion Sensor mode INPUT_PULLUP
  pinMode(motionSensor, INPUT_PULLUP);
  // Set motionSensor pin as interrupt, assign interrupt function and set RISING mode
  attachInterrupt(digitalPinToInterrupt(motionSensor), detectsMovement, RISING);

  // Set LED to LOW
  pinMode(led, OUTPUT);
  digitalWrite(led, LOW);
}

void loop() {
  // Current time
  now = millis();
  if((digitalRead(led) == HIGH) && (motion == false)) {
    Serial.println("MOTION DETECTED!!!");
    motion = true;
  }
  // Turn off the LED after the number of seconds defined in the timeSeconds variable
  if(startTimer && (now - lastTrigger > (timeSeconds*1000))) {
    Serial.println("Motion stopped...");
    digitalWrite(led, LOW);
    startTimer = false;
    motion = false;
  }
}

*/

#include <Arduino.h>
#include <IRrecv.h>
#include <IRutils.h>

const int led = 20;

/******
DECLARAÇÃO DAS VARIÁVEIS DE TEMPERATURA E UMIDADE
******/
#include "DHTStable.h"
DHTStable DHT;
#define DHT11_PIN       21

void ler_DHT() {
  int chk = DHT.read11(DHT11_PIN);
  switch (chk)
  {
    case DHTLIB_OK:  
      Serial.print("OK,\t"); 
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
  Serial.print(DHT.getHumidity(), 1);
  Serial.print(",\t");
  Serial.println(DHT.getTemperature(), 1);
  delay(2000);
}


/******
DECLARAÇÃO DA FUNÇÃO DE INTERRUPÇÃO VIA BOTÃO
******/
#define pushButton_pin   15

int i=0;

void IRAM_ATTR toggleLED()
{
  #ifdef RGB_BUILTIN
    digitalWrite(RGB_BUILTIN, HIGH);   // Turn the RGB LED white
    delay(1000);
    digitalWrite(RGB_BUILTIN, LOW);    // Turn the RGB LED off
    delay(1000);
  #endif

}

/******
DECLARAÇÃO DAS VARIÁVEIS DO SENSOR DE MOVIMENTO
******/

#define timeSeconds 4

const int motionSensor = 19;

// Timer: Auxiliary variables
unsigned long now = millis();
unsigned long lastTrigger = 0;
boolean startTimer = false;
boolean motion = false;

// CASO MOVIMMENTO SEJA DETECTADO
void IRAM_ATTR detectsMovement() {
  digitalWrite(led, HIGH);
  startTimer = true;
  lastTrigger = millis();
}

void ler_Movimento(){
  now = millis();
  if((digitalRead(led) == HIGH) && (motion == false)) {
    Serial.println("MOTION DETECTED!!!");
    motion = true;
  }
  // Turn off the LED after the number of seconds defined in the timeSeconds variable
  if(startTimer && (now - lastTrigger > (timeSeconds*1000))) {
    Serial.println("Motion stopped...");
    digitalWrite(led, LOW);
    startTimer = false;
    motion = false;
  }
}

/******
DECLARAÇÃO DAS VARIÁVEIS DE COMUNICAÇÃO IR
******/

const int kRecvPin = 47;
const uint16_t kCaptureBufferSize = 1024;
const uint8_t kTimeout = 50; // or 15

// Objeto para receber e decodificar sinais IR
IRrecv irrecv(kRecvPin, kCaptureBufferSize,  kTimeout, true);
decode_results results;

void ler_SinalIR(){
  if (irrecv.decode(&results)) {
    Serial.println(resultToHumanReadableBasic(&results));
    Serial.println("Source Code: ");
    Serial.println(resultToSourceCode(&results));
    // Limpar o buffer de recepção
    irrecv.resume();
  }
  delay(100);
}

void setup() {
  // Iniciar comunicação serial
  Serial.begin(115200);

  // Declaração do botão para interrupção externa [TESTE]
  pinMode(pushButton_pin, INPUT);
  attachInterrupt(pushButton_pin, toggleLED, RISING);

  // PIR Motion Sensor mode INPUT_PULLUP
  pinMode(motionSensor, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(motionSensor), detectsMovement, RISING);

  // LED DE TESTE
  pinMode(led, OUTPUT);
  digitalWrite(led, LOW);

  // Configurar o pino do receptor IR
  pinMode(kRecvPin, INPUT);
  // Iniciar o receptor IR
  irrecv.enableIRIn();
}

void loop() {
  // Verificar se um sinal IR foi recebido
  ler_SinalIR();

  ler_Movimento();

  ler_DHT();

}







