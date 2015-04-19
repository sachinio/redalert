__author__ = 'sachinpatney'

import subprocess, os

broadcast_address = '00 00 00 00 00 00 FF FF'
repo_root = '/var/www/git/redalert'

units = [
    {
        'id' : 0,
        'addr' : '00 00 00 00 00 00 FF FF',
        'email': 'spatney@microsoft.com'
    }
]


def notifyOfBreak(culprits):
    stillUnit(broadcast_address, 500, 20, '255, 0, 0', 5)
    for c in culprits:
        for u in units:
            if c == u['email']:
                glowUnit(u['addr'], 500, 100, '255, 0, 0', 5)


def glowUnit(addr, delay, bri, color, tout):
    os.chdir(os.path.join([repo_root,'/apis/lights']))
    subprocess.call(['python', 'lights.py', addr, 'G', delay, bri, color, tout])


def stillUnit(addr, delay, bri, color, tout):
    os.chdir(os.path.join([repo_root,'/apis/lights']))
    subprocess.call(['python', 'lights.py', addr, 'S', delay, bri, color, tout])


def stopAll():
    subprocess.call(['python', 'lights.py', broadcast_address, 'O', '500', '100', '0, 0, 0', '0'])