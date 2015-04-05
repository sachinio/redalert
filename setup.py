from __future__ import print_function # Py3 print fx

# This file will aid in installing all required
# frameworks/libraries

from subprocess import call
import os
import time
import fileinput

print("Setting things up for you.. go grab a coffee or something!")

time.sleep(2)

cw = os.getcwd();

# Get latest
call(['sudo','apt-get','update']);
# Install required libraries
call(['sudo','apt-get','install','apache2', 'php5', 'libapache2-mod-php5','git','mpg123','-y'])
# Update OS/Libraries
call(['sudo','apt-get','upgrade','-y'])
os.chdir('/var/www')
call('sudo mkdir git'.split(' '))
call('sudo mkdir ram'.split(' '))
os.chdir('git')
call('sudo git clone https://github.com/silvanmelchior/RPi_Cam_Web_Interface.git cam'.split(' '))
os.chdir('cam')
for line in fileinput.input('RPi_Cam_Web_Interface_Installer.sh', inplace=True):
    print(line.replace('rpicamdir=""', 'rpicamdir="rpicam"'),end='')
call('chmod u+x RPi_Cam_Web_Interface_Installer.sh'.split(' '))
call(['./RPi_Cam_Web_Interface_Installer.sh','install'])

for line in fileinput.input('/etc/raspimjpeg', inplace=True):
    print(line.replace('preview_path /dev/shm/mjpeg/cam.jpg', 'preview_path /var/www/ram/cam.jpg'),end='')

for line in fileinput.input('/etc/raspimjpeg', inplace=True):
    print(line.replace('divider 1', 'divider 5'),end='')

for line in fileinput.input('/etc/raspimjpeg', inplace=True):
    print(line.replace('rotation 0', 'rotation 90'),end='')

os.chdir('../')
call('sudo git clone https://github.com/sachinio/redalert.git redalert'.split(' '))
os.chdir('redalert/camera')
print('Compiling servo.c')
call('sudo gcc -o servo servo.c -lwiringPi'.split(' '))
os.chdir('../../')
call('git clone https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code.git adafruit'.split(' '))
call(['sudo','rm', '-rf', cw])

# other thinsgs to automate
# 1. add apache to sudo
# 2. create temp fs for camera
# 3. Add crone jobs for server