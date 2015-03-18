'''Virtual Theremin'''
fs          = 44100 # Sampling Rate
nChannels   = 1     # Number of Audio channels
sampleWidth = 2     # Number of Bytes per sample
chunkSize   = 1024  # Chunk Size


import sys
import pyaudio
import soundgenerators
import helpers


def virtualTheremin():
    # Init PyAudio
    p = pyaudio.PyAudio()

    # Open up output stream
    stream = p.open(format=p.get_format_from_width(sampleWidth),
                    channels=nChannels,
                    rate=fs,
                    output=True)

    # Init Theremin
    theremin = soundgenerators.Theremin()
    theremin.volume = 0.4

    try:
        # Main Loop
        while True:
            '''
                Edit Theremin Paramters Here. Examples:
                - Ascending Frequency:
                    theremin.frequency = 220 * (1 + helpers.ascending())

                - Ascending Vibrato Intensity:
                    theremin.vibratoAmount = helpers.ascending(0.1)

                - Tremolo Intensity:
                    theremin.tremoloAmount = helpers.ascending(2)
            '''
            v = helpers.ascending() # An ascending float value over time 0<=v
            theremin.frequency = 220 * (1 + 0.5*v)
            theremin.morph = max(0, 1-abs(v-1))
            theremin.tremoloAmount = max(0, 1-abs(v-2))

            signal = theremin.read()
            data = helpers.convert(signal)
            stream.write(data)

    except (KeyboardInterrupt):
        # Cleanup
        stream.stop_stream()
        stream.close()
        p.terminate()
        sys.exit(0)

    sys.exit(-1)


if __name__ == '__main__':
    virtualTheremin()
