# This file will aid in installing all required
# frameworks/libraries

# IMPORTANT NOTE: Call this from the Redalert GIT root

from subprocess import call
import os
import time

print "Setting things up for you.. go grab a coffee or something!"

time.sleep(2)

cw = os.getcwd();

# Get latest
#call(['sudo','apt-get','update']);
# Install required libraries
#call(['sudo','apt-get','install','apache2', 'php5', 'libapache2-mod-php5','git','mpg123','-y'])
# Update OS/Libraries
#call(['sudo','apt-get','upgrade','-y'])
os.chdir('/var/www')
call('sudo mkdir git'.split(' '))
os.chdir('git')
call('git clone https://github.com/sachinio/redalert.git redalert'.split(' '))
os.chdir('redalert/camera')
print 'Compiling servo.c'
call('sudo gcc -o servo servo.c -lwiringPi'.split(' '))
os.chdir('../../')
call('git clone https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code.git adafruit'.split(' '))

call(['sudo','rm', '-rf', cw])

# other thinsgs to automate
# 1. add apache to sudo
# 2. create temp fs for camera
# 3. Add crone jobs for server