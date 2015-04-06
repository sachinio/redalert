from __future__ import print_function # Py3 print fx

# This file will aid in installing all required
# frameworks/libraries

from subprocess import call
import os
import time
import fileinput
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--delete", help="remove dir after install", action="store_true")
parser.add_argument("-r", "--rotation", help="rotation of the camera", action="store", default='0')
parser.add_argument("-s", "--skipupdate", help="skip update", action="store_true")

args = parser.parse_args()

print("Setting things up for you... go grab a coffee or something?")

time.sleep(2)

cwd = os.getcwd()

if not args.skipupdate:
    # Get latest
    print('\nGetting latest ... \n')
    call(['sudo','apt-get','update'])

    # Install/Upgrade required libraries
    print('\nInstalling & upgrading required libraries ...\n')

    call(['sudo','apt-get','install','apache2', 'php5', 'libapache2-mod-php5', 'git', 'mpg123' , 'pip', '-y'])
    call('sudo pip install pyusb'.split(' '))
    call(['sudo','apt-get','upgrade','-y'])
else:
    print('Skipping update ...')

os.chdir('/var/www')

call('sudo mkdir git'.split(' '))
call('sudo mkdir ram'.split(' '))

os.chdir('git')

print('\nInstalling Cam Interface ...\n')

call('sudo git clone https://github.com/silvanmelchior/RPi_Cam_Web_Interface.git cam'.split(' '))
os.chdir('cam')
call('sudo git pull'.split(' '))

for line in fileinput.input('RPi_Cam_Web_Interface_Installer.sh', inplace=True):
    print(line.replace('rpicamdir=""', 'rpicamdir="rpicam"'),end='')

call('chmod u+x RPi_Cam_Web_Interface_Installer.sh'.split(' '))
call(['./RPi_Cam_Web_Interface_Installer.sh', 'install'])

for line in fileinput.input('/etc/raspimjpeg', inplace=True):
    print(line.replace('preview_path /dev/shm/mjpeg/cam.jpg', 'preview_path /var/www/ram/cam.jpg'),end='')

for line in fileinput.input('/etc/raspimjpeg', inplace=True):
    print(line.replace('divider 1', 'divider 5'),end='')

for line in fileinput.input('/etc/raspimjpeg', inplace=True):
    print(line.replace('rotation 0', 'rotation '+args.rotation),end='')

call(['sudo','./RPi_Cam_Web_Interface_Installer.sh', 'autostart_no'])

print('\nInstalling Red Alert ...\n')

os.chdir('../')
call('sudo git clone https://github.com/sachinio/redalert.git redalert'.split(' '))
os.chdir('redalert')
call('sudo git pull'.split(' '))
os.chdir('camera')

print('\nCompiling Servo.c ...\n')

call('sudo gcc -o servo servo.c -lwiringPi'.split(' '))

print('\nInstalling Adafruit Servo library ...\n')

os.chdir('../../')
call('git clone https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code.git adafruit'.split(' '))
os.chdir('adafruit')
call('sudo git pull'.split(' '))

if(args.delete):
    call(['sudo','rm', '-rf', cwd])
print('\nSetup is complete!')

# other thinsgs to automate
# 1. add apache to sudo
# 2. create temp fs for camera
# 3. Add crone jobs for server