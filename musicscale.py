'''Music scale

Fit continous frequency into music scales.
'''
from helpers import freq_2_midi, midi_2_freq

# Scale Patterns
_chroma_pattern = range(12)
_major_pattern = [0, 2, 4, 5, 7, 9, 11]
_minor_pattern = [0, 2, 3, 5, 7, 8, 10]
_pentatonic_pattern = [0, 2, 4, 7, 9]

def _scale_builder(pattern, maxD=128):
    n = len(pattern)
    idx = n - 1
    ret = []
    for i in range(maxD):
        if i % 12 in pattern:
            idx = (idx + 1) % n

        ret.append(pattern[idx] + 12 * (i / 12))
    return ret

# Build Mapping
_chroma_map = _scale_builder(_chroma_pattern)
_major_map = _scale_builder(_major_pattern)
_minor_map = _scale_builder(_minor_pattern)
_pentatonic_map = _scale_builder(_pentatonic_pattern)


def _scaler(mapping):
    '''Returns function with mapping'''
    def inner(freq):
        d = freq_2_midi(freq)
        d_scaled = mapping[d]
        return midi_2_freq(d_scaled)
    return inner


'''Scaling functions'''
scale_to_chroma = _scaler(_chroma_map)
scale_to_major = _scaler(_major_map)
scale_to_minor = _scaler(_minor_map)
scale_to_pentatonic = _scaler(_pentatonic_map)


def no_scaling(f):
    return f
