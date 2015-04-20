__author__ = 'sachinpatney'

import sys
import urllib2, time

sys.path.append('/var/www/git/redalert/tasks')

from common import EMail
from subprocess import check_output

time.sleep(10)  # Let WIFI Connect

ifconfig = check_output(["ifconfig"])

public_ip = 'Could not be determined'
try:
    public_ip = urllib2.urlopen('http://ip.42.pl/raw').read()
except:
    print 'Could not determine public IP, only sending ifconfig.'

out = "ifconfig\n------------------------------\n\n {0}\n\nPublic IP: {1}".format(ifconfig, public_ip)

EMail('Red Alert controller boot info', out).send()