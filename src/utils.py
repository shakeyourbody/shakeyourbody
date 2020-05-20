from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])


def run_safe(f, *args):
    if callable(f):
        return f(*args)
