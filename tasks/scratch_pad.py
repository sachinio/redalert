__author__ = 'sachinpatney'

# Just a test area for scripts

import binascii


def cal_checksum(data):
    checksum = 0
    arr = []
    for a in data:
        arr.append(a)

    arr.reverse()

    while len(arr) > 0:
        h = ((arr.pop() + arr.pop()).encode('utf-8'))
        checksum += int(h, 16)

    return hex(int('0xFF', 16)-int(str(hex(checksum))[-2:], 16))

# s = b'7E000A010150010048656C6C6FB8'
s = b'7e001090007d33a20040bf8e93b303025041554cb0'

data = s[32:-2]
print('Expected Checksum -> ' + cal_checksum(s[6:-2].decode('utf-8')))
print('Data -> ' + binascii.unhexlify(data).decode('utf-8'))
print(b'checksum -> ' + s[-2:])
