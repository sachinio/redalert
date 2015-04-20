__author__ = 'sachinpatney'


import smtplib, sys

sys.path.append('/var/www/git/redalert/tasks')

import common
from subprocess import check_output

fromaddr = 'sachinpatney@gmail.com'
toaddrs = 'sachinpatney@gmail.com'

out = check_output(["ifconfig"])
header = 'To:' + toaddrs + '\n' + 'From: ' + fromaddr + '\n' + 'Subject:Raspberry Pi IP\n'
msg = header + out

# Credentials (if needed)
cred = common.sync_read_status_file()

username = cred['gmail_username']
password = cred['gmail_password']

# The actual mail send
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(username,password)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()