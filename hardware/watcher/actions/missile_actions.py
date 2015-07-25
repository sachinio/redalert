__author__ = 'sachinpatney'

from actions_common import IAction
import subprocess

class FireMissile(IAction):
    def __init__(self):
        pass

    def __do__(self):
        print('Firing Missile')
        subprocess.call(['sudo', 'python3', '/var/www/git/redalert/hardware/missile/missile.py', 'fire', '1'])
        pass