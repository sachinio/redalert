__author__ = 'sachinpatney'

import datetime
import time
from speak import say

say('Hello Seattle')

while True:
    hm = datetime.datetime.now().strftime('%H,%M').split(',')
    if hm[0] == '01' and hm[1] == '02':
        print 'new hour'
        break
    else:
        print 'tick tock'
    time.sleep(30)