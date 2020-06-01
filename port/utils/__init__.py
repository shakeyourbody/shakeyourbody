from collections import namedtuple
import struct


def bits2float(b):
    s = struct.pack('>l', b)
    return struct.unpack('>f', s)[0]


def chain(*rings):
    def chained(*args):
        for ring in rings:
            ring(*args)
    return chained
