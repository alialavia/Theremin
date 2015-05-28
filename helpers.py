import sys
import os
import inspect
import struct
import numpy as np
import config


def freq_2_midi(f):
    '''Converts frequency to MIDI number'''
    return int(round(69 + 12 * np.log2(f / float(config.a440))))


def midi_2_freq(d):
    '''Converts MIDI number to frequency'''
    return np.power(2., (d - 69) / 12.) * config.a440


_notelist = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def freq_2_note(f):
    '''Converts frequency to note name'''
    d = freq_2_midi(f)
    return _notelist[d % 12]


def add_leap_path():
    src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
    arch_dir = 'lib/x64' if sys.maxsize > 2 ** 32 else 'lib/x86'
    sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))


def cutoff(value, minCut, maxCut):
    '''value -> range [minCut, maxCut]'''
    return max(minCut, min(maxCut, value))


_maxVal = 2 ** (config.sampleWidth * 8) / 2.1


def convert(seq):
    '''Converts numpy float array ([-1.0, 1.0]) to binary data (little
    endian).
    '''
    seq2 = _maxVal * seq
    fmt = '<' + len(seq) * 'h'
    return struct.pack(fmt, *seq2)


def print_on_same_line(string):
    '''Put Cursor back one line and print'''
    sys.stdout.write('\r' + str(string))
    sys.stdout.flush()
