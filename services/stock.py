__author__ = 'sachinpatney'

from common import IMonaJob
from common import Mona

import urllib2, random

template = "Microsoft stock closed at {0}, {1}, {2}."
motivate = ['come on people we can do better!']
praise = ['Great job guys!']

class StockInfo(IMonaJob):
    def __run__(self, time):
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