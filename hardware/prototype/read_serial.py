__author__ = 'sachinpatney'

import serial
import time
import binascii

ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1.0)

s = b''

while True:
        bytesToRead = ser.inWaiting()

        if bytesToRead > 0:
            s += ser.read()
            w = ser.read(2)
            s += w
            l = int.from_bytes(w, byteorder='big')
            print('len: '+str(l))
            s += ser.read(l)
        else:
            if len(s) > 0:
                print('Hex string')
                print(binascii.hexlify(s))
            s = b''
