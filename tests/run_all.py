__author__ = 'sachinpatney'

from unittest import defaultTestLoader
from unittest import TextTestRunner

suite = defaultTestLoader.discover('.')

TextTestRunner().run(suite)