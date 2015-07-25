#include <XBee.h>

XBee xbee = XBee();
const int buttonPin = 7;     // the number of the pushbutton pin
int buttonState; 
int lastButtonState = LOW;
long lastDebounceTime = 0;  // the last time the output pin was toggled
long debounceDelay = 50;    // the debounce time; increase if the output flickers
void setup() {
  Serial.begin(9600);
  xbee.setSerial(Serial);
  pinMode(buttonPin, INPUT);  
}

void send(String s){
  uint8_t p = '\0';
  uint8_t payload[] = {p,p,p,p,p,p,p,p,p,p,p,p};
  
  s.getBytes(payload, sizeof(payload));

  XBeeAddress64 addr64 = XBeeAddress64(0x00000000, 0x00000000);
  ZBTxRequest zbTx = ZBTxRequest(addr64, payload, sizeof(payload));
  
  xbee.send(zbTx);
}

void loop() {
  int reading = digitalRead(buttonPin);

  if (reading != lastButtonState) {
    lastDebounceTime = millis();
  } 
  
  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (reading != buttonState) {
      buttonState = reading;

      if (buttonState == LOW) {
        send("fire");
      }
    }
  }
  
  lastButtonState = reading;
}