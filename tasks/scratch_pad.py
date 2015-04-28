__author__ = 'sachinpatney'

# Just a test area for scripts

from datetime import datetime
from urllib.request import urlopen

l = datetime.now().strftime('%H,%M').split(',')

options = {
    'hour': l[0],
    'min': l[1]
}

print(urlopen("http://finance.yahoo.com/d/quotes.csv?s=MSFT&f=spc1").read())