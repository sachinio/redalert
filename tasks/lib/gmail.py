__author__ = 'sachinpatney'


import smtplib, sys

sys.path.append('/var/www/git/redalert/tasks')

import common
from common import TMP_FOLDER_PATH
from subprocess import check_output

fromaddr = 'sachinpatney@gmail.com'
toaddrs = 'sachinpatney@gmail.com'

out = check_output(["ifconfig"])

msg = out

# Credentials (if needed)
cred = common.read_csv(TMP_FOLDER_PATH + '/gmailcred.csv')

username = cred['username']
password = cred['password']

# The actual mail send
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(username,password)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()