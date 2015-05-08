#include <XBee.h>

XBee xbee = XBee();


void setup() {
  Serial.begin(9600);
  xbee.setSerial(Serial);
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
  send("play");
  delay(5000);
}