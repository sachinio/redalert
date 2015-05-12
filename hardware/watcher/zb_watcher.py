__author__ = 'sachinpatney'

import sys
sys.path.append('/var/www/git/redalert/tasks')

import serial
import time
import binascii
from test_action import LetsParty


ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1.0)
s = b''


def do(command):
    if command == 'party':
        LetsParty().__do__()


while True:
        bytesToRead = ser.inWaiting()

        if bytesToRead > 0:
            s += ser.read()
            if binascii.hexlify(s) == b'7e':
                w = ser.read(2)
                s += w
                l = int(binascii.hexlify(w), 16)
                s += ser.read(l + 2)
                s = binascii.hexlify(s)

                if s[6:8] == b'90':  # Receive Request, checksum verification not needed.
                    data = s[32:-2]
                    data = binascii.unhexlify(data).decode('utf-8').strip('\0')
                    do(data)
            else:
                s = b''
        else:
            s = b''
            time.sleep(0.3)

do('party')