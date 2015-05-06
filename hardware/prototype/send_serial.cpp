#include <XBee.h>

XBee xbee = XBee();

uint8_t payload[] = { 0, 0 };

XBeeAddress64 addr64 = XBeeAddress64(0x0013a200, 0x403e0f30);
ZBTxRequest zbTx = ZBTxRequest(addr64, payload, sizeof(payload));
ZBTxStatusResponse txStatus = ZBTxStatusResponse();


void setup() {
  Serial.begin(9600);
  xbee.setSerial(Serial);
}

void loop() {
  payload[0] = 6;
  payload[1] = 9;

  xbee.send(zbTx);

  delay(1000);
}