#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <softPwm.h>

int main(int argc, char *argv[]){
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
  int newPos = 6 + (17 * pos/180);
  softPwmWrite(pin, newPos);
  delay(tdelay);
  return 0;
}