__author__ = 'sachinpatney'

import os, subprocess
repo_root = '/var/www/git/redalert'


class Mona:
    @staticmethod
    def switchToMonaDir():
        os.chdir(repo_root + '/apis/mona')

    @staticmethod
    def joke():
        Mona.switchToMonaDir()
        subprocess.call(['sudo', 'php', 'play_sound_cmd', repo_root+'/resources/sounds/newword.mp3'])

    @staticmethod
    def speak(msg):
        Mona.switchToMonaDir()
        subprocess.call(['sudo', 'python', 'google.py', msg])


class IMonaJob():

    def __run__(self, time, lock):
        """Runs the job"""
        raise Exception('You must implement __run__ method on your service')