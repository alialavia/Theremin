'''Configuration Paramters'''
# Sampling Rate
fs = 44100

# Number of Audio channels
nChannels = 1

# Number of Bytes per sample
sampleWidth = 2

# Chunk Size
chunkSize = 256

# Minimum frequency of Virtual Theremin [Hz]
# 261.626 Hz ~ C4/Middle C
fmin = 261.626

# Maximum frequency of Virtual Theremin [Hz]
# fmax = 2 * fmin -> one octave
fmax = 2 * fmin

# Kammerton A440 [Hz]
a440 = 440.
