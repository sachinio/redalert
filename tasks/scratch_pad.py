__author__ = 'sachinpatney'

# Just a test area for scripts

import binascii
s = b'7e001090007d33a20040bf8e93b303025041554cb0'

t = s[6:8]

print(t)

data = s[32:-2]



print('Data -> ' + binascii.unhexlify(data).decode('utf-8'))

print(s[-2:])
