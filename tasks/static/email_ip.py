__author__ = 'sachinpatney'

import sys
import urllib2, time

sys.path.append('/var/www/git/redalert/tasks')

from common import EMail
from subprocess import check_output
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-w", "--skipwifi", help="skip waiting for wifi to log on",
                    action="store_true")
parser.add_argument("-s", "--skippublicip", help="skip getting public ip",
                    action="store_true")

args = parser.parse_args()

if not args.skipwifi
    time.sleep(10)  # Let WIFI Connect

ifconfig = check_output(["ifconfig"])

public_ip = 'Could not be determined'
if not args.skippublicip:
    try:
        public_ip = urllib2.urlopen('http://ip.42.pl/raw').read()
    except:
        print 'Could not determine public IP, only sending ifconfig.'

out = "ifconfig\n------------------------------\n\n {0}\n\nPublic IP: {1}".format(ifconfig, public_ip)

EMail('Red Alert controller boot info', out).send()