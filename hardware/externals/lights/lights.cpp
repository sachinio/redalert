#include <Adafruit_NeoPixel.h>
#include <avr/power.h>
#include <XBee.h>

#define PIN       6
#define NUMPIXELS 8

char MSG[25], CMD[30];
int DEL = 100, BRI = 20, R = 255, G = 100, B = 50, TOUT = 5;
int x;
long t;

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

XBee xbee = XBee();
XBeeResponse response = XBeeResponse();
ZBRxResponse rx = ZBRxResponse();
ModemStatusResponse msr = ModemStatusResponse();

void setup() {
  pixels.begin(); 
  t = millis() + TOUT * 1000;
  CMD[0] = 'F';
  
  //Change to Serial1 if using micro
  Serial.begin(9600); 
  xbee.begin(Serial);
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
      
      if (xbee.getResponse().getApiId() == ZB_RX_RESPONSE) {
        xbee.getResponse().getZBRxResponse(rx);
            
        if (rx.getOption() == ZB_PACKET_ACKNOWLEDGED) {
        } else {}
        
        int len = rx.getDataLength();
        char m[len+1];
        for(int i=0;i<len;i++){
          m[i]=rx.getData(i);
        }
        m[len]='\0';

        splitString(m, CMD,DEL,BRI, R, G ,B, TOUT);
        t=millis() + TOUT * 1000;
        
      } else if (xbee.getResponse().getApiId() == MODEM_STATUS_RESPONSE) {
        xbee.getResponse().getModemStatusResponse(msr);
        if (msr.getStatus() == ASSOCIATED) {} 
        else if (msr.getStatus() == DISASSOCIATED) {} 
        else {}
      } else {}
    } else if (xbee.getResponse().isError()) {}
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
    case 'D': disco(DEL, BRI);
    break;
    case 'G': glow(DEL, BRI);
    break;
    case 'O': 
    default: off();
  }
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
  int d = del/(100 * bri/100);
  if(d < 1){
    d=1;
  }
  
  for(int i=0;i<NUMPIXELS;i++){
    pixels.setPixelColor(i, R,G,B);
  }
  
  while(cb<bri){
    cb++;
    pixels.setBrightness(cb);
    pixels.show();
    delay(d);
  }
  
  while(cb>1){
    cb--;
    pixels.setBrightness(cb);
    pixels.show();
    delay(d);
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
  
  int len = 40;
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