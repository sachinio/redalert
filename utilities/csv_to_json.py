__author__ = 'sachinpatney'

import json
import sys

sys.path.append('/var/www/git/redalert/tasks')

from common import read_csv_as_list

print(json.dumps(read_csv_as_list(sys.argv[1])))