__author__ = 'sachinpatney'


import sys

sys.path.append('/var/www/git/redalert/tasks')

from common import Timeline

name = sys.argv[1]
title = sys.argv[2]
content = sys.argv[3]
img = None

if len(sys.argv) > 4:
    img = sys.argv[4]

Timeline.add_item(name, title, content, img)