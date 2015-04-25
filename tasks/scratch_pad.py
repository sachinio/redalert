__author__ = 'sachinpatney'

# Just a test area for scripts

from datetime import datetime

l = datetime.now().strftime('%H,%M').split(',')

options = {'hour': l[0], 'min': l[1]}

print options