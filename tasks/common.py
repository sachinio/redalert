__author__ = 'sachinpatney'

import os, subprocess, random, csv

from threading import Lock

REPOSITORY_ROOT = '/var/www/git/redalert'
TMP_FOLDER_PATH = '/var/www/tmp'

TALKING_PILLOW = Lock()


class IMonaTask():
    def __run__(self, time):
        """Runs the job"""
        raise Exception('You must implement __run__ method on your service')


def switch_to_mona_path():
    os.chdir(REPOSITORY_ROOT + '/apis/mona')


def read_csv(path):
    reader = csv.reader(open(path, 'rb'))
    return dict(x for x in reader)


def write_to_csv(dict, path):
    writer = csv.writer(open(path, 'wb'))
    for key, value in dict.items():
        writer.writerow([key, value])


class Mona:
    @staticmethod
    def play_sound(name):
        TALKING_PILLOW.acquire()
        subprocess.call(['sudo','pkill','omxplayer'])
        subprocess.call(['sudo','omxplayer',name])
        TALKING_PILLOW.release()

    @staticmethod
    def speak(msg):
        TALKING_PILLOW.acquire()
        switch_to_mona_path()
        subprocess.call(['sudo', 'python', 'mona.py', msg])
        TALKING_PILLOW.release()


class BuildNotifier:
    broadcast_address = '00 00 00 00 00 00 FF FF'

    statusFile = REPOSITORY_ROOT + '/vso_status.csv'

    units = [
        {
            'id' : 0,
            'addr' : '00 00 00 00 00 00 FF FF',
            'email': 'spatney@microsoft.com'
        }
    ]

    @staticmethod
    def wasBroken():
        return read_csv(BuildNotifier.statusFile).broken

    @staticmethod
    def writeStatus(status):
        write_to_csv({'broken': status})


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
        BuildNotifier.stillUnit(BuildNotifier.broadcast_address, '10', '10', '0, 255, 0', '5')

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
        os.chdir(REPOSITORY_ROOT + '/apis/lights')

    @staticmethod
    def stopAll():
        subprocess.call(['python', 'lights.py', BuildNotifier.broadcast_address, 'O', '500', '100', '0, 0, 0', '0'])