__author__ = 'sachinpatney'

import serial
import time
import binascii

ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1.0)

s = b''

while True:
        bytesToRead = ser.inWaiting()

        if bytesToRead > 0:
            w = ser.read(3)
            s += w
            l = int.from_bytes(w[2] + w[3], byteorder='big')
            print('len: '+l)
            s += ser.read(l)
        else:
            if len(s) > 0:
                print('Hex string')
                print(binascii.hexlify(s))
            s = b''
