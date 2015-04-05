# This file will aid in installing all required
# frameworks/libraries

from subprocess import call
import os
import time

print "Setting things up for you.. go grab a coffee or something!"

time.sleep(2)

#call(['sudo','apt-get','update']);
#call(['sudo','apt-get','install','apache2', 'php5', 'libapache2-mod-php5','git','mpg123','-y'])
#call(['sudo','apt-get','upgrade','-y'])
os.chdir('../')
call('git clone https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code.git'.split(' '))