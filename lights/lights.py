from __future__ import print_function
import serial
import time
import sys

def calChecksum(frameData):
    checksum=0
    for a in frameData:
        checksum+=int(a,16)
    return hex(int('0xFF',16)-int(str(hex(checksum))[-2:],16))

def createFrame(address, data):
    frameDelimiter = "7E"
    frameType = "10"
    frameId = "01"
    destAdd = "FF FE"
    broadcastR = "00"
    options = "00"

    d = ' '.join([frameType, frameId, address, destAdd, broadcastR, options]);
    arr = d.split(' ')
    for a in data:
        arr.append(a.encode("hex"))

    checksum = calChecksum(arr)
    arr = arr[::-1]
    arr.append(hex(len(arr)))
    arr.append("00")
    arr.append(frameDelimiter)
    arr = arr[::-1]
    arr.append(checksum)
    cmd = ''.join(chr(int(b,16)) for b in arr)

    return cmd

ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=3.0);

address = "00 13 A2 00 40 C1 AC 62"
data = sys.argv[1]+","+sys.argv[2]+",20,100,40,0,3"

frame = createFrame(address, data)
ser.write(frame)
ser.close()
