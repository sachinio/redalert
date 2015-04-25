__author__ = 'sachinpatney'


import sys

sys.path.append('/var/www/git/redalert/tasks')

from common import Timeline

name = sys.argv[1]
title = sys.argv[2]
content = sys.argv[3]
icon = sys.argv[4]
iconBack = sys.argv[5]
img = ''

if len(sys.argv) > 6:
    img = sys.argv[6]

Timeline.add_item(name, title, content, img, icon, iconBack)