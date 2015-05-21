'''Virtual Theremin'''
fs          = 44100 # Sampling Rate
nChannels   = 1     # Number of Audio channels
sampleWidth = 2     # Number of Bytes per sample
chunkSize   = 1024  # Chunk Size
baseNote = 220            #baseNote Note frequency

import sys
import pyaudio
import soundgenerators
import helpers
import Leap, HandProcessor

def printInfo(theremin):
    print helpers.freqency_to_note(theremin.frequency), " Freq = ", theremin.frequency, ", Volume =", theremin.volume
    #print helpers.freqency_to_note(theremin.frequency)

# Handler for left hand
def lefthand(hand):
    handState = HandProcessor.HandState(hand)
    print handState.Pinch

# Handler for right hand
def righthand(hand):
    handState = HandProcessor.HandState(hand)
    print handState.Pinch

def initialize():    
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
    theremin.frequency = 220

    # Init Leap
    handprocessor = HandProcessor.HandProcessor()

    # Attach handlers to right and left hand events
    handprocessor.attachLeftEventHandler(lefthand)
    handprocessor.attachRightEventHandler(righthand)
    handprocessor.run()
    return p, stream, theremin

def virtualTheremin():
    
    p, stream, theremin = initialize()


    try:
        # Main Loop
        while True:        
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
