__author__ = 'sachinpatney'

from common import IMonaTask
from common import Timeline

import datetime
import random

class DaysToGA(IMonaTask):
    def __run__(self, time):
        if time[0] == '00' and time[1] == '14':
            d0 = datetime.datetime.now().date()
            d1 = datetime.date(2015,7,24)
            delta = d1 - d0
            Timeline.add_item('Mona',
                              '{0} days to GA :)'.format(delta.days),
                              '',
                               random.choice(['owl.gif','owl2.gif]),
                              'fa-bullhorn',
                              'info')
