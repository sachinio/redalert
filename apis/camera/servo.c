/*
Servo control via a software PWM,
since raspberry pi lacks a hardware one

This is designed specifically for one servo type,
change MIN & MAX for other types
*/

#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <softPwm.h>

int main(int argc, char *argv[]){
  int MIN=6;
  int MAX=17;
  int tdelay = 800;
  if(argc <  3){
    printf("Insuffcient args. servo [angle] [pin] [?delay]\n");
    return;
  }
  int pin=atoi(argv[2]);
  if(wiringPiSetup() == -1)
    exit(1);
  if(argc == 4)
    tdelay=atoi(argv[3]);
  softPwmCreate(pin,0,200);

  int pos = atoi(argv[1]);
  int newPos = MIN + (MAX * pos/180);
  softPwmWrite(pin, newPos);
  delay(tdelay);
  printf("servo is now at %s",argv[1]);
  return 0;
}