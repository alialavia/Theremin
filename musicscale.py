from numpy import log2, power
a440 = 440.
maxD = 128

_chroma_map    = []

_major_pattern = {1, 3, 6, 8, 10}
_major_map     = []

_minor_pattern = {1, 4, 6, 9, 11}
_minor_map     = []

_pentatonic_pattern  = {1, 3, 8}
_pentatonic_pattern2 = {6, 11}
_pentatonic_map      = []


for i in range(maxD):
    _chroma_map.append(i)

    if i % 12 in _major_pattern:
        _major_map.append(i-1)

    else:
        _major_map.append(i)

    if i % 12 in _minor_pattern:
        _minor_map.append(i-1)

    else:
        _minor_map.append(i)

    if i % 12 in _pentatonic_pattern:
        _pentatonic_map.append(i-1)

    elif i % 12 in _pentatonic_pattern2:
        _pentatonic_map.append(i-2)

    else:
        _pentatonic_map.append(i)


def freq_2_midi(f):
    return int(69 + 12 * log2(f / a440))

def midi_2_freq(d):
    return power(2., (d - 69) / 12.) * a440

def _scaler(mapping):
    def inner(freq):
        d = freq_2_midi(freq)
        d_scaled = mapping[d]
        return midi_2_freq(d_scaled)
    return inner

scale_to_chroma     = _scaler(_chroma_map)
scale_to_major      = _scaler(_major_map)
scale_to_minor      = _scaler(_minor_map)
scale_to_pentatonic = _scaler(_pentatonic_map)

def no_scaling(f):
    return f
