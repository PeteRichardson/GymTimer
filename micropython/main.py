""" counter.py - counts to 9999 and rolls over to 0 """

import time
import random
from display import Display

def random_color():
    """ pick a random color.   Not that this won't matter when displaying values < 5,
        which are forced to red currently """
    g = random.randint(0,255)
    r = random.randint(0,255)
    b = random.randint(0,255)
    return (g, r, b)

counter = Display(270, 28, 8, "clock")    # clock mode means show 01:01 instead of 00:61
SECS = 0
while True :
    counter.show(SECS, 1, color = random_color() )
    time.sleep(1.0)
    SECS = (SECS + 1) % 10000
