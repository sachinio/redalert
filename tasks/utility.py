__author__ = 'sachinpatney'

# Just a test area for scripts

import json
from common import read_csv_as_list

l = read_csv_as_list('/var/www/tmp/timeline.csv')

print l

print json.dumps(l)
