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


def sync_write_to_file(name, operation, message):
    with open(name, operation) as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        f.write(message)


class Mona:
    rooms = ['3A', '3B', '3C']  # for future use
    room_ip = {  # for future use
        '3A': '',
        '3B': '',
        '3C': 'localhost'
    }

    @classmethod
    def play_sound(cls, name):
        TALKING_PILLOW.acquire()
        subprocess.call(['sudo','pkill','omxplayer'])
        subprocess.call(['sudo','omxplayer',name])
        TALKING_PILLOW.release()

    @classmethod
    def speak(cls, msg):
        TALKING_PILLOW.acquire()
        switch_to_mona_path()
        subprocess.call(['sudo', 'python', 'mona.py', msg])
        TALKING_PILLOW.release()


class BuildNotifier:
    broadcast_address = '00 00 00 00 00 00 FF FF'

    statusFile = TMP_FOLDER_PATH + '/vso_status.csv'

    units = [
        {
            'id' : 0,
            'addr' : '00 00 00 00 00 00 FF FF',
            'email': 'spatney@microsoft.com',
            'room': '3C'
        }
    ]

    @classmethod
    def wasBroken(cls):
        return read_csv(cls.statusFile)['broken'] == 'True'

    @classmethod
    def writeStatus(cls, status):
        write_to_csv({'broken': status}, cls.statusFile)


    @classmethod
    def notify_build_break(cls, culprits):
        BuildNotifier.still_unit(cls.broadcast_address, '10', '20', '255, 0, 0', '0')
        for c in culprits:
            for u in cls.units:
                if c['uniqueName'] == u['email']:
                    cls.glow_unit(u['addr'], '500', '100', '255, 0, 0', '0')

        #cls.announce_build_break()
        #Mona.speak(culprits[0]['displayName'] + ', could you please fix it!')

    @classmethod
    def announce_build_break(cls):
        Mona.speak('Attention. This is an important message. There has been a build break!')

    @classmethod
    def notify_all_clear(cls):
        cls.still_unit(cls.broadcast_address, '10', '10', '0, 255, 0', '5')

    @classmethod
    def glow_unit(cls, addr, delay, bri, color, tout):
        cls.switch_to_lights_path()
        subprocess.call(['python', 'lights.py', addr, 'G', delay, bri, color, tout])

    @classmethod
    def still_unit(cls, addr, delay, bri, color, tout):
        cls.switch_to_lights_path()
        subprocess.call(['python', 'lights.py', addr, 'S', delay, bri, color, tout])

    @classmethod
    def switch_to_lights_path(cls):
        os.chdir(REPOSITORY_ROOT + '/apis/lights')

    @classmethod
    def off_all_lights(cls):
        subprocess.call(['python', 'lights.py', cls.broadcast_address, 'O', '500', '100', '0, 0, 0', '0'])