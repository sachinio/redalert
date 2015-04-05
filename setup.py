# This file will aid in installing all required
# frameworks/libraries

from subprocess import call

call(['sudo','apt-get','update']);
call(['sudo','apt-get','install','apache2', 'php5', 'libapache2-mod-php5','git','mpg123','-y'])
call(['sudo','apt-get','upgrade','-y'])
call(['sudo','mkdir','../servoboard'])