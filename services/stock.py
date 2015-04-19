__author__ = 'sachinpatney'

from common import IMonaTask
from common import Mona

import urllib2, random

template = "Microsoft stock closed at {0}, {1}, {2}."
motivate = ['come on people we can do better!', 'OK. Clearly you guys need to work harder.']
praise = ['Great job guys!', 'Well done! Go treat yourself to some coffee.']

class StockInfo(IMonaTask):
    def __run__(self, time):
        if (time[0] == '16' and time[1] == '15') or True:
            result = urllib2.urlopen("http://finance.yahoo.com/d/quotes.csv?s=MSFT&f=spc1").read()
            result = result.strip().split(',')

            dir = 'down'

            if float(result[2]) > 0:
                dir = 'up'

            msg = template.format(result[1].replace('.',' point '), dir, result[2].replace('.',' point ').replace('-', ''))
            Mona.speak(msg)

            if dir == 'up':
                Mona.speak(random.choice(praise))
            else:
                Mona.speak(random.choice(motivate))