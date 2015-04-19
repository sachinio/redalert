__author__ = 'sachinpatney'

import os, subprocess
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
        Mona.playSound(repo_root+'/resources/sounds/newword.mp3')

    @staticmethod
    def speak(msg):
        switchToMonaDir()
        subprocess.call(['sudo', 'python', 'google.py', msg])


class IMonaJob():

    def __run__(self, time, lock):
        """Runs the job"""
        raise Exception('You must implement __run__ method on your service')