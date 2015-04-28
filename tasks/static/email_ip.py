__author__ = 'sachinpatney'

import sys
import time
import argparse

sys.path.append('/var/www/git/redalert/tasks')

from urllib.request import urlopen
from common import EMail
from subprocess import check_output

parser = argparse.ArgumentParser()
parser.add_argument("-w", "--wifi", help="wait for wifi to log on", action="store_true")
parser.add_argument("-p", "--public_ip", help="include public ip", action="store_true")

args = parser.parse_args()

if args.wifi:
    time.sleep(10)  # Wait for WIFI to connect

ifconfig = check_output(["ifconfig"])

public_ip = 'Not requested'
if args.public_ip:
    try:
        public_ip = urlopen('http://ip.42.pl/raw').read()
    except:
        public_ip = 'Could not determine Public IP'

out = "Hey, I just rebooted, and here is some info!" \
      "\n\nifconfig\n------------------------------\n\n {0}\n\n" \
      "Public IP: {1}".format(ifconfig, public_ip)

EMail('onBoot info', out).send()