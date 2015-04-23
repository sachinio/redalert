__author__ = 'sachinpatney'

# Just a test area for scripts
from common import Mona
from common import REPOSITORY_ROOT;
from vso import VSO

print len(VSO().get_broken_builds(VSO().get_build_info()))