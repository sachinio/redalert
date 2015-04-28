import fcntl
import sys
import codecs

import serial
import binascii

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

    d = ' '.join([frameType, frameId, address, destAdd, broadcastR, options])
    arr = d.split(' ')
    for a in data:
        arr.append(str(binascii.hexlify(a.encode('utf-8')), 'ascii'))

    checksum = calChecksum(arr)
    arr = arr[::-1]
    arr.append(str(hex(len(arr))).replace('0x',''))
    arr.append("00")
    arr.append(frameDelimiter)
    arr = arr[::-1]
    arr.append(str(checksum).replace('0x',''))
    print(arr)
    cmd = ''.join(b for b in arr)

    return cmd

address = sys.argv[1]
data = sys.argv[2]+","+sys.argv[3]+","+sys.argv[4]+","+sys.argv[5]+","+sys.argv[6]

frame = createFrame(address, data)

ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=3.0)
fcntl.flock(ser.fileno(), fcntl.LOCK_EX)
ser.write(bytearray.fromhex(frame))
print(frame)
print(bytearray.fromhex(frame))
print(sys.argv)
