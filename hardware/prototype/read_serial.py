__author__ = 'sachinpatney'

import serial

ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1.0)

while True:
    try:
        bytesToRead = ser.inWaiting()
        if bytesToRead > 0:
            s = ser.read(bytesToRead)
            print(s)
    except:
        print('Exception .. timeout ?')
