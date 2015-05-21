import sys
import struct
from time import time
from main import sampleWidth
import Leap

_maxVal = 2 ** (sampleWidth * 8) / 2.1
_notelist = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'G#', 'A', 'Bb', 'B']

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


def distance_to_frequency(d):
    ''' Calculates frequency of a note d half steps away from A4 (440 Hz) '''
    return 440.0 * pow(2.0, d / 12.0)


def note_to_frequency(note, octave):    
    ''' Calculates frequency of note in octave '''
    if note in _notelist:
        # Calculate distance from A4
        d = (_notelist.index(note) - 9) + (12 * (octave - 4))
        return distance_to_frequency(d)
    else:
        raise ValueError('Note should be one of these string values:' + ', '.join(_notelist))


            