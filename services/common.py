__author__ = 'sachinpatney'

import os, subprocess, random
repo_root = '/var/www/git/redalert'


def switchToMonaDir():
    os.chdir(repo_root + '/apis/mona')


class Mona:

    @staticmethod
    def playSound(name):
        subprocess.call(['sudo','pkill','omxplayer'])
        subprocess.call(['sudo','omxplayer',name])

    @staticmethod
    def joke():
        jokes = ['newword.mp3','policechief.mp3']
        Mona.playSound(repo_root+'/resources/sounds/'+random.choice(jokes))

    @staticmethod
    def speak(msg):
        switchToMonaDir()
        subprocess.call(['sudo', 'python', 'google.py', msg])


class IMonaJob():

    def __run__(self, time, lock):
        """Runs the job"""
        raise Exception('You must implement __run__ method on your service')


class BuildNotifier:
    broadcast_address = '00 00 00 00 00 00 FF FF'

    units = [
        {
            'id' : 0,
            'addr' : '00 00 00 00 00 00 FF FF',
            'email': 'spatney@microsoft.com'
        }
    ]

    @staticmethod
    def notifyOfBreak(culprits):
        BuildNotifier.stillUnit(BuildNotifier.broadcast_address, '10', '20', '255, 0, 0', '0')
        for c in culprits:
            for u in BuildNotifier.units:
                if c['uniqueName'] == u['email']:
                    BuildNotifier.glowUnit(u['addr'], '500', '100', '255, 0, 0', '0')

        BuildNotifier.announceBuildBreak()
        Mona.speak(culprits[0]['displayName'] + ', could you please fix it!')

    @staticmethod
    def announceBuildBreak():
        Mona.speak('Attention. This is an important message. There has been a build break!')

    @staticmethod
    def notifyAllClear():
        BuildNotifier.stillUnit(BuildNotifier.broadcast_address, '10', '10', '0, 255, 0', '0')

    @staticmethod
    def glowUnit(addr, delay, bri, color, tout):
        BuildNotifier.switchToLightDir()
        subprocess.call(['python', 'lights.py', addr, 'G', delay, bri, color, tout])

    @staticmethod
    def stillUnit(addr, delay, bri, color, tout):
        BuildNotifier.switchToLightDir()
        subprocess.call(['python', 'lights.py', addr, 'S', delay, bri, color, tout])

    @staticmethod
    def switchToLightDir():
        os.chdir(repo_root + '/apis/lights')

    @staticmethod
    def stopAll():
        subprocess.call(['python', 'lights.py', BuildNotifier.broadcast_address, 'O', '500', '100', '0, 0, 0', '0'])