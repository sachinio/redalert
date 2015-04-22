__author__ = 'sachinpatney'

import json, sys
from common import read_csv_as_list

sys.path.append('/var/www/git/redalert/tasks')
print json.dumps(read_csv_as_list(sys.argv[1]))