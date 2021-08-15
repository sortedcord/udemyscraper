from alive_progress import alive_bar

import time


def compute():
    for i in range(1000):
        x = 2  # process an item
        yield  # insert this and you're done!


with alive_bar(1000) as bar:
    for i in compute():
        bar()
