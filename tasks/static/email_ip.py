__author__ = 'sachinpatney'

sys.path.append('/var/www/git/redalert/tasks')

from common import EMail
from subprocess import check_output

out = check_output(["ifconfig"])

EMail('Red Alert controller boot info', out).send()