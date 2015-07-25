__author__ = 'sachinpatney'

import sys
sys.path.append('/var/www/git/redalert/tasks')
sys.path.append('/var/www/git/redalert/hardware/watcher/actions')

import serial
import time
import binascii
from party_actions import LetsParty
from missile_actions import FireMissile

ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1.0)
s = b''


def do(command):
    if command == 'party':
        LetsParty().__do__()
    if command == 'fire':
        FireMissile().__do__()

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
            time.sleep(0.2)
