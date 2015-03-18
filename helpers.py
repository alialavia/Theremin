import sys
import struct
from time import time
from main import sampleWidth


_maxVal = 2 ** (sampleWidth * 8) / 2.1
def convert(seq):
    '''Converts numpy float array ([-1.0, 1.0]) to binary data (little endian)'''
    seq2 = _maxVal * seq
    fmt = '<' + len(seq) * 'h'
    return struct.pack(fmt, *seq2)


_t0 = time()
def ascending(m=5.0):
    '''Ascending float value'''
    return (time() - _t0) / m


def descending(m=5.0):
    '''Descending float value'''
    return 1.0 - (time() - _t0) / m


def print_on_same_line(fVal):
    '''Put Cursor back one line and print'''
    sys.stdout.write('\r%.4f' % fVal)
    sys.stdout.flush()
