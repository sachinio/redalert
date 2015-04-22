__author__ = 'sachinpatney'

# Just a test area for scripts
from common import Mona
from common import REPOSITORY_ROOT;
import random
jokes = ['newword.mp3', 'policechief.mp3', 'antimatte.mp3']
Mona.play_sound(REPOSITORY_ROOT+'/resources/sounds/'+random.choice(jokes))