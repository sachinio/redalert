/* For Arduino Micro */

#include <Adafruit_GFX.h>
#include <Adafruit_NeoMatrix.h>
#include <Adafruit_NeoPixel.h>
#include <avr/power.h>
#include <XBee.h>

#define PIN       6
#define NUMPIXELS 64

char MSG[25], CMD[30];
int DEL = 100, BRI = 20, R = 255, G = 100, B = 50, TOUT = 0;
int x;
long t;
Adafruit_NeoMatrix pixels = Adafruit_NeoMatrix(8, 8 , PIN,
  NEO_MATRIX_TOP     + NEO_MATRIX_RIGHT +
  NEO_MATRIX_COLUMNS + NEO_MATRIX_PROGRESSIVE,
  NEO_GRB            + NEO_KHZ800);
//Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

XBee xbee = XBee();
XBeeResponse response = XBeeResponse();
ZBRxResponse rx = ZBRxResponse();
ModemStatusResponse msr = ModemStatusResponse();

uint8_t payload[] = { 0, 0 };
XBeeAddress64 addr64 = XBeeAddress64(0x0013a200, 0x40c1aaed);
ZBTxRequest zbTx = ZBTxRequest(addr64, payload, sizeof(payload));
  
void setup() {
  pixels.begin(); 
  CMD[0] = 'O';
  Serial1.begin(9600); 
  Serial.begin(9600);
  setupAPI();
  setupMatrix();
}

void setupAPI(){
  xbee.begin(Serial1);
}

void setupMatrix(){
  pixels.begin();
  pixels.setTextWrap(false);
  pixels.setBrightness(5);
}

void checkTimeout(){
  if(TOUT == 0)
    return;
  if(millis()>t)
    CMD[0] = 'O';
}
void checkSerialAPI(){
    xbee.readPacket();
    
    if (xbee.getResponse().isAvailable()) {
      // got something
      Serial.println("GOT SOMETHING");
      
      if (xbee.getResponse().getApiId() == ZB_RX_RESPONSE) {
        // got a zb rx packet
        
        // now fill our zb rx class
        xbee.getResponse().getZBRxResponse(rx);
            
        if (rx.getOption() == ZB_PACKET_ACKNOWLEDGED) {
            //Serial.println("Sender got it");
        } else {
            //Serial.println("Sender did not get it");
        }
        
        int len = rx.getDataLength();
        char m[len+1];
        for(int i=0;i<len;i++){
          m[i]=rx.getData(i);
        }
        m[len]='\0';

        splitString(m, CMD,DEL,BRI, R, G ,B, TOUT);
        t=millis() + TOUT * 1000;
        //payload[0] = 'O';
        //payload[1] = 'K';
        //xbee.send(zbTx);
        
      } else if (xbee.getResponse().getApiId() == MODEM_STATUS_RESPONSE) {
        xbee.getResponse().getModemStatusResponse(msr);
        // the local XBee sends this response on certain events, like association/dissociation
        
        if (msr.getStatus() == ASSOCIATED) {
          Serial.println("ASSOCIATED");
        } else if (msr.getStatus() == DISASSOCIATED) {
          Serial.println("DISASSOCIATED");
        } else {
          Serial.println("Something Else");  
        }
      } else {
      	Serial.println("Not expecting this");  
      }
    } else if (xbee.getResponse().isError()) {
      Serial.println("xbee.getResponse().isError()");  
    }
}

int checkSerial() {
  int i=0;
  if (Serial1.available()) {
    delay(50);
    while(Serial1.available()) {
      MSG[i++] = Serial1.read();
    }
    MSG[i++]='\0';
  }
}

void showMsg(int bri) {
  pixels.setBrightness(bri);
  pixels.setTextColor(pixels.Color(255, 0, 0));
  pixels.fillScreen(0);
  pixels.setCursor(x, 0);
  char msgStr[30];
  int i=1;
  while(CMD[i] != '\0'){
    msgStr[i-1] = CMD[i];
    i++;
  }
  int len = i*6;
  msgStr[i-1] = '\0';
  pixels.print(msgStr);
  if(--x < -len) {
    x = pixels.width();
  }
  pixels.show();
  delay(DEL);
}

void loop() {
  checkSerialAPI();
  checkTimeout();      
  switch(toupper(CMD[0])){
    case 'R': runningLights(DEL, BRI);
    break;
    case 'F': flashingLights(DEL, BRI);
    break;
    case 'P': police(DEL, BRI);
    break;
    case 'S': still(BRI);
    break;
    case 'M': showMsg(BRI);
    break;
    case 'D': disco(DEL, BRI);
    break;
    case 'G': glow(DEL, BRI);
    break;
    case 'O': off();
  }
  //wordloop();
}

void off(){
  for(int i=0;i<NUMPIXELS;i++){
    pixels.setPixelColor(i,0,0,0);
  }
  pixels.show();
}

void police(int del, int bri){
  pixels.setBrightness(bri);
  int delFac = 6;
  
  for(int k=0; k<6; k++){
    if(k==3){
      delay(del*delFac);
    }
    if(k<3){
      for(int i=0;i<NUMPIXELS/2;i++){
        pixels.setPixelColor(i, 255,0,0);
      }
    }
    else{
      for(int i=NUMPIXELS/2;i<NUMPIXELS;i++){
        pixels.setPixelColor(i, 0,0,255);
      }
    }
  
    pixels.show();
    delay(del);
    
    for(int i=0;i<NUMPIXELS;i++){
      pixels.setPixelColor(i, 0,0,0);

    }
    
    pixels.show();
    delay(del/2);
  }
  
  delay(del * delFac);
}

void still(int brightness){
  pixels.setBrightness(brightness);
    for(int i=0;i<NUMPIXELS;i++){
    pixels.setPixelColor(i, R,G,B);
  }
  pixels.show();
}

void flashingLights(int del, int brightness){
  pixels.setBrightness(brightness);
  for(int i=0;i<NUMPIXELS;i++){
    pixels.setPixelColor(i, R,G,B);
  }
  
  pixels.show();
  delay(del);
  for(int i=0;i<NUMPIXELS;i++){
    pixels.setPixelColor(i, 0,0,0);
  }
  
  pixels.show();
  delay(del);
}

void glow(int del, int bri){
  int cb = 0;
  for(int i=0;i<NUMPIXELS;i++){
    pixels.setPixelColor(i, R,G,B);
  }
  
  while(cb<bri){
    pixels.setBrightness(++cb);
    pixels.show();
    delay(del/(100 * bri/100));
  }
  
  while(cb>0){
    pixels.setBrightness(cb--);
    pixels.show();
    delay(del/(100 * bri/100));
  }
}

void runningLights(int del, int brightness){
    pixels.setBrightness(brightness);
    for(int i=0;i<NUMPIXELS;i++){
      pixels.setPixelColor(i, R, G, B);
      if(i!=0){
        pixels.setPixelColor(i-1, 0,0,0);
      }
      pixels.show();
      delay(del);
      pixels.setPixelColor(NUMPIXELS-1, 0,0,0);
    }
}

void disco(int del, int brightness){
  pixels.setBrightness(brightness);
  
  for(int i=0;i<NUMPIXELS;i++){
    int ran = random(0,2);
    if(ran == 0){
        int r = random(0,256);
        int g = random(0,256);
        int b = random(0,256);
        pixels.setPixelColor(i,r,g,b);
    }
  }
  pixels.show();
  delay(del * random(1,4));
  for(int i=0;i<NUMPIXELS;i++){
    int ran = random(0,4);
    if(ran !=0){
        int r = random(0,256);
        int g = random(0,256);
        int b = random(0,256);
        pixels.setPixelColor(i,0,0,0);
    }
  }
  pixels.show();
  delay(del * random(1,3));
}

void splitString(char* chars, char* cmd, int &num1, int &num2, int &num3, int &num4, int &num5, int &num6) {
  const int MaxValLen = 25;
  char val1[MaxValLen]={};
  char val2[MaxValLen]={};
  char val3[MaxValLen]={};
  char val4[MaxValLen]={};
  char val5[MaxValLen]={};
  char val6[MaxValLen]={};
  
  int len = 25;
  int i=0;
  int j=0;

  while(chars[i] != ',' && i<len){ 
    cmd[j] = chars[i];
    i++; j++;
  }
  
  cmd[j]='\0';
  i++;j=0;
  
  while(chars[i] != ',' && i<len){
    val1[j] = chars[i];
    i++; j++;
  }
  
  val1[j] = '\0';
  num1 = atoi(val1);
  i++; j=0;
  
  while(chars[i] != ',' && i<len){
    val2[j] = chars[i];
    i++; j++;
  }
  
  val2[j] = '\0';
  num2 = atoi(val2);
  i++; j=0;
  
  while(chars[i] != ',' && i<len){
    val3[j] = chars[i];
    i++; j++;
  }
  
  val3[j] = '\0';
  num3 = atoi(val3);
  i++; j=0;
  
  while(chars[i] != ',' && i<len){
    val4[j] = chars[i];
    i++; j++;
  }
  
  val4[j] = '\0';
  num4 = atoi(val4);
  i++; j=0;
  
  while(chars[i] != ',' && i<len){
    val5[j] = chars[i];
    i++; j++;
  }
  
  val5[j] = '\0';
  num5 = atoi(val5);
  i++; j=0;
  
  while(chars[i] != ',' && i<len){
    val6[j] = chars[i];
    i++; j++;
  }
  
  val6[j] = '\0';
  num6 = atoi(val6);
  i++; j=0;
}