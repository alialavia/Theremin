'''Music scale

Fit continous frequency into music scales.
- no_scaling:          No scaling, continous frequencies
- scale_to_chroma:     12 step chromatic scale
- scale_to_major:      C major scale
- scale_to_minor:      C minor scale
- scale_to_pentatonic: C pentatonic scale
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


def _scale_to_func(mapping):
    '''Returns function with mapping'''
    def inner(freq):
        d = freq_2_midi(freq)
        d_scaled = mapping[d]
        return midi_2_freq(d_scaled)

    return inner


'''Scaling functions'''
scale_to_chroma = _scale_to_func(_chroma_map)
scale_to_major = _scale_to_func(_major_map)
scale_to_minor = _scale_to_func(_minor_map)
scale_to_pentatonic = _scale_to_func(_pentatonic_map)


def no_scaling(f):
    return f
