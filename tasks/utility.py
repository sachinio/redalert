__author__ = 'sachinpatney'

# Just a test area for scripts
from common import Mona
from common import REPOSITORY_ROOT;
from vso import VSO

import datetime

d0 = datetime.datetime.now().date()
d1 = datetime.date(2015,7,24)
delta = d1 - d0
print '{0} days to GA!'.format(str(delta.days))

print datetime.datetime.now().strftime('%H,%M').split(',')