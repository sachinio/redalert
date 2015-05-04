# This will help setup the entire redalert installation
# on a raspberry pi

from subprocess import call
import os
import shutil
import time
import fileinput
import argparse

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def copy_bot_images():
    src = '/var/www/git/redalert/assets/images'
    dest = '/var/www/uploads/redbull'
    src_files = os.listdir(src)
    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, dest)

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--skipupdate", help="skip update",
                    action="store_true")
parser.add_argument("-d", "--delete", help="remove dir containing setup.py after install",
                    action="store_true")
parser.add_argument("-r", "--rotation", help="rotation of the camera", action="store",
                    default='0')
parser.add_argument("-c", "--cron", help="enable cron jobs", action="store_true")

args = parser.parse_args()

print("Setting things up for you... go grab a "+color.BOLD+'coffee'+color.END+" or something?")

time.sleep(2)

cwd = os.getcwd()

if not args.skipupdate:
    # Get latest
    print('\nGetting latest ... \n')
    call(['sudo','apt-get','update'])
    call(['sudo','apt-get','upgrade','-y'])
else:
    print('\nSkipping update ...\n')

# Install/Upgrade required libraries
print('\nInstalling & upgrading required libraries ...\n')

packs = ['apache2', 'php5', 'libapache2-mod-php5', 'git', 'mpg123', 'python3-pip']

for pack in packs:
    call(['sudo', 'apt-get', 'install',pack,'-y'])

call('sudo pip-3.2 install pyusb'.split(' '))
call('sudo pip-3.2 install pyserial'.split(' '))

os.chdir('/var/www')

call('sudo mkdir git'.split(' '))
call('sudo mkdir ram'.split(' '))
call('sudo mkdir uploads'.split(' '))
os.chdir('uploads')
call('sudo mkdir bot'.split(' '))
os.chdir('../')
call('sudo mkdir tmp'.split(' '))
call('sudo chmod 0777 -R /var/www/uploads/'.split(' '))

hasRam = False
with open('/etc/fstab', 'r') as inF:
    for line in inF:
        if 'tmpfs /var/www/ram' in line:
            hasRam = True

if not hasRam:
    print('\nCreating a temporary file system (RAM) ...\n')
    with open("/etc/fstab", "a") as myfile:
        myfile.write("tmpfs /var/www/ram tmpfs nodev,nosuid,size=1M 0 0")
else:
    print('\nRam already added to tempfs')

apacheHasPerms = False
with open('/etc/sudoers', 'r') as inF:
    for line in inF:
        if 'www-data ALL=(ALL) NOPASSWD: ALL' in line:
            apacheHasPerms = True

if not apacheHasPerms:
    print('\nGranting Apache Sudo Permissions ...\n')
    with open("/etc/sudoers", "a") as myfile:
        myfile.write("www-data ALL=(ALL) NOPASSWD: ALL")
else:
    print('\nApache already has permissions\n')

os.chdir('git')

print('\nInstalling Cam Interface ...\n')

call('sudo git clone https://github.com/silvanmelchior/RPi_Cam_Web_Interface.git cam'.split(' '))
os.chdir('cam')
call('sudo git pull'.split(' '))

for line in fileinput.input('RPi_Cam_Web_Interface_Installer.sh', inplace=True):
    print(line.replace('rpicamdir=""', 'rpicamdir="rpicam"'), end='')

call('chmod u+x RPi_Cam_Web_Interface_Installer.sh'.split(' '))
call(['./RPi_Cam_Web_Interface_Installer.sh', 'install'])

for line in fileinput.input('/etc/raspimjpeg', inplace=True):
    print(line.replace('preview_path /dev/shm/mjpeg/cam.jpg', 'preview_path /var/www/ram/cam.jpg'), end='')

for line in fileinput.input('/etc/raspimjpeg', inplace=True):
    print(line.replace('divider 1', 'divider 5'), end='')

for line in fileinput.input('/etc/raspimjpeg', inplace=True):
    print(line.replace('rotation 0', 'rotation '+args.rotation), end='')

call(['sudo','./RPi_Cam_Web_Interface_Installer.sh', 'autostart_no'])


print('\nInstalling Adafruit Servo library ...\n')

os.chdir('../')
call('sudo git clone https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code.git adafruit'.split(' '))
os.chdir('adafruit')
call('sudo git pull'.split(' '))

os.chdir('../')
call('sudo git clone git://git.drogon.net/wiringPi'.split(' '))
os.chdir('wiringPi')
call('sudo git pull origin'.split(' '))
call('./build'.split(' '))

print('\nInstalling Red Alert ...\n')

os.chdir('../')
call('sudo git clone https://github.com/sachinio/redalert.git redalert'.split(' '))
os.chdir('redalert')
call('sudo git pull'.split(' '))
os.chdir('hardware/camera')

print('\nCompiling Servo.c ...\n')

call('sudo gcc -o servo servo.c -lwiringPi'.split(' '))

copy_bot_images()

if(args.cron):
    print('Yet to do!')

if(args.delete):
    call(['sudo','rm', '-rf', cwd])
print('\nSetup is complete ' + color.BOLD + color.GREEN +':)' + color.END )

if not hasRam or not apacheHasPerms or args.cron:
    print('You will need to '+color.BOLD +'reboot' + color.END + ' your system for stuff to work correctly ')