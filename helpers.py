import sys, os, inspect
import struct
import config

_notelist = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def addLeapPath():
    src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
    arch_dir = 'lib/x64' if sys.maxsize > 2**32 else 'lib/x86'
    sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

def cutoff(value, minCut, maxCut):
    '''value -> range [minCut, maxCut]'''
    return max(minCut, min(maxCut, value))

_maxVal = 2 ** (config.sampleWidth * 8) / 2.1

def convert(seq):
    # Needed in __main__.py
    '''Converts numpy float array ([-1.0, 1.0]) to binary data (little endian)'''
    seq2 = _maxVal * seq
    fmt = '<' + len(seq) * 'h'
    return struct.pack(fmt, *seq2)

def print_on_same_line(fVal):
    '''Put Cursor back one line and print'''
    sys.stdout.write('\r%.4f' % fVal)
    sys.stdout.flush()
