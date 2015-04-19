__author__ = 'sachinpatney'

import subprocess, os
from common import Mona

broadcast_address = '00 00 00 00 00 00 FF FF'

units = [
    {
        'id' : 0,
        'addr' : '00 00 00 00 00 00 FF FF',
        'email': 'spatney@microsoft.com'
    }
]


def notifyOfBreak(culprits):
    stillUnit(broadcast_address, '10', '20', '255, 0, 0', '0')
    for c in culprits:
        for u in units:
            if c['uniqueName'] == u['email']:
                glowUnit(u['addr'], '500', '100', '255, 0, 0', '0')

    announceBuildBreak()
    Mona.speak(culprits[0]['displayName'] + ', could you please fix it.')


def announceBuildBreak():
    Mona.speak('Attention. This is an important message. There has been a build break.')


def notifyAllClear():
    stillUnit(broadcast_address, '10', '10', '0, 255, 0', '0')

def glowUnit(addr, delay, bri, color, tout):
    switchToLightDir()
    subprocess.call(['python', 'lights.py', addr, 'G', delay, bri, color, tout])


def stillUnit(addr, delay, bri, color, tout):
    switchToLightDir()
    subprocess.call(['python', 'lights.py', addr, 'S', delay, bri, color, tout])


def switchToLightDir():
    os.chdir(repo_root + '/apis/lights')

def stopAll():
    subprocess.call(['python', 'lights.py', broadcast_address, 'O', '500', '100', '0, 0, 0', '0'])