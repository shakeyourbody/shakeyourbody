from collections import namedtuple
import struct

Point = namedtuple('Point', ['x', 'y'])


def run_safe(f, *args):
    if callable(f):
        return f(*args)


def bits2float(b):
    s = struct.pack('>l', b)
    return struct.unpack('>f', s)[0]
