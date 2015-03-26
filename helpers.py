import sys
import struct
from time import time
from main import sampleWidth
import Leap

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

def freqency_to_note(freq):
    freqlist = [16.35,17.32,18.35,19.45,20.60,21.83,23.12,24.50,25.96,27.50,29.14,30.87
    ,32.70,34.65,36.71,38.89,41.20,43.65,46.25,49.00,51.91,55.00,58.27,61.74
    ,65.41,69.30,73.42,77.78,82.41,87.31,92.50,98.00,103.8,110.0,116.5,123.5
    ,130.8,138.6,146.8,155.6,164.8,174.6,185.0,196.0,207.7,220.0,233.1,246.9
    ,261.6,277.2,293.7,311.1,329.6,349.2,370.0,392.0,415.3,440.0,466.2,493.9
    ,523.3,554.4,587.3,622.3,659.3,698.5,740.0,784.0,830.6,880.0,932.3,987.8
    ,1047, 1109, 1175, 1245, 1319, 1397, 1480, 1568, 1661, 1760, 1865, 1976
    ,2093, 2217, 2349, 2489, 2637, 2794, 2960, 3136, 3322, 3520, 3729, 3951
    ,4186, 4435, 4699, 4978, 5274, 5588, 5920, 6272, 6645, 7040, 7459, 7902]

    notelist = ['C','C#','D', 'Eb','E', 'F', 'F#','G', 'G#','A', 'Bb', 'B']

    nearestFreq = min(freqlist, key=lambda x:abs(x-freq))

    findindex = freqlist.index(nearestFreq)
    notename = int(findindex % 12)
    octave = int(findindex / 12)
    return notelist[notename] + str(octave)


def findPinch(hand):
    iterfingers = iter(hand.fingers)
    thumb = hand.fingers[0]
    thumbbone = thumb.bone(Leap.Bone.TYPE_DISTAL)
    #print "%f" % (hand.pinch_strength * 100.0),
    distances = []           
    if (thumbbone.is_valid):
        next(iterfingers)
        distances = []
        for finger in iterfingers:
            fingerbone = finger.bone(Leap.Bone.TYPE_DISTAL)                                        
            if (fingerbone.is_valid):                        
                distances += [fingerbone.next_joint.distance_to(thumbbone.next_joint)]
        minDistance = min(distances)
    
    if distances == [] or minDistance > 45:
        return -1
    
    return distances.index(minDistance)


def maxDistance(hand):
    distances = []
    interaction_box = hand.frame.interaction_box

    for finger in hand.fingers:
        fingerbone = finger.bone(Leap.Bone.TYPE_DISTAL)                                        
        if (fingerbone.is_valid):                        
            distances += [interaction_box.normalize_point(fingerbone.next_joint).z]

    return max(distances)

            