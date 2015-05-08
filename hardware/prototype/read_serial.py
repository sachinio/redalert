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

                s += ser.read(l + 2)
                s = binascii.hexlify(s)

                if s[6:8] == b'90':
                    data = s[32:-2]
                    print('Data -> ' + binascii.unhexlify(data).decode('utf-8'))
                else:
                    print(s[6:8])
                    print('Unknown Type')
            else:
                s = b''
        else:
            s = b''
            time.sleep(0.3)
