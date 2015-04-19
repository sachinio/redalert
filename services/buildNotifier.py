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
    stillUnit(broadcast_address, '10', '20', '255, 0, 0', '5')
    for c in culprits:
        for u in units:
            if c['uniqueName'] == u['email']:
                glowUnit(u['addr'], '500', '100', '255, 0, 0', '5')

    announceBuildBreak()
    announce(culprits[0]['displayName'] + ' please fix it')


def announce(msg):
    os.chdir(repo_root + '/apis/mona')
    subprocess.call(['sudo', 'python', 'google.py', msg])


def announceBuildBreak():
    announce('Attention. This is an important message. There has been a build break')


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