__author__ = 'sachinpatney'

import subprocess, os

units = [
    {
        'id' : 0,
        'addr' : '00 00 00 00 00 00 FF FF',
        'email': 'spatney@microsoft.com'
    }
]

def notifyOfBreak(culprits):
    u = units[0]
    os.chdir('../apis/lights')
    subprocess.call(['python', 'lights.py', u['addr'], 'G', '500', '100', '255, 0, 0', '5'])