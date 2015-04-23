__author__ = 'sachinpatney'

from common import IMonaTask
from common import Timeline

import datetime


class DaysToGA(IMonaTask):
    def __run__(self, time):
        if time[0] == 0 and time[1] == 0:
            d0 = datetime.datetime.now().date()
            d1 = datetime.date(2015,7,24)
            delta = d1 - d0
            print delta.days
            Timeline.add_item('mona', '{0} days to GA!'.format(str(delta.days)),
                              '',
                              'owl.gif', 'fa-bullhorn',
                              'info')