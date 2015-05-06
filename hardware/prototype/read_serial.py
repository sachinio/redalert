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
            if binascii.hexlify(s) == b'7e':
                w = ser.read(2)
                s += w
                l = int(binascii.hexlify(w), 16)
                print('len: '+str(l))
                s += ser.read(l)
            else:
                s = b''
        else:
            if len(s) > 0:
                print('Hex string')
                print(binascii.hexlify(s))
            s = b''
