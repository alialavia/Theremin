'''Virtual Theremin'''
from settings import *
import sys
import pyaudio
import soundgenerators
import helpers
import musicscale

helpers.addLeapPath()
import Leap, HandProcessor


# Paramters
fmin = 261.626 # [Hz]
fmax = fmin * 2 # [Hz]

# Init
#global theremin
theremin = soundgenerators.Theremin()
theremin.volume = 0.4
theremin.frequency = 220
#global scaling_func
scaling_func = musicscale.no_scaling

def printInfo(theremin):
    print helpers.freqency_to_note(theremin.frequency), " Freq = ", theremin.frequency, ", Volume =", theremin.volume
    #print helpers.freqency_to_note(theremin.frequency)



# Handler for left hand
def lefthand(hand):
    handState = HandProcessor.HandState(hand)
    global theremin, scaling_func
    # Pinching
    p = handState.Pinch
    print "Left  ", handState.Pinch, handState.PalmState
    if p != -1:
        if p == 0:
            scaling_func = musicscale.no_scaling
        elif p == 1:
            scaling_func = musicscale.scale_to_chroma
        elif p == 2:
            scaling_func = musicscale.scale_to_major
        elif p == 3:
            scaling_func = musicscale.scale_to_pentatonic

    # Open/Closed Hand
    a = handState.PalmState
    theremin.tremoloAmount = 1 - a

    # Position -> Vol
    x, y, z = handState.PalmPosition
    theremin.volume = y
    

# Handler for right hand
def righthand(hand):
    handState = HandProcessor.HandState(hand)
    global theremin, scaling_func
    print "Right ", handState.Pinch, handState.PalmState

    # Pinching
    p = handState.Pinch
    if p != -1:
        theremin._Theremin__osc1.waveformFunc = [soundgenerators.sin, soundgenerators.triangle, 
                                      soundgenerators.sawtooth, soundgenerators.square][p]
    
    # Open/Closed Hand
    a = handState.PalmState
    theremin.vibratoAmount = (1 - a) * 10
    
    # Position -> freq
    x, y, z = handState.PalmPosition
    freq = fmin + (1.0-z) * fmax
    theremin.frequency = scaling_func(freq)

    


def virtualTheremin(): 
    try:
           # Init PyAudio
        p = pyaudio.PyAudio()

        # Open up output stream
        stream = p.open(format=p.get_format_from_width(sampleWidth),
                        channels=nChannels,
                        rate=fs,
                        output=True)


        # Init Leap
        print "Initializing Leap"
        handprocessor = HandProcessor.HandProcessor()
        print "Done"

        # Attach handlers to right and left hand events
        handprocessor.attachLeftEventHandler(lefthand)
        handprocessor.attachRightEventHandler(righthand)
        handprocessor.run()

        # Main Loop
        while True:        
            signal = theremin.read()
            data = helpers.convert(signal)
            stream.write(data)

    except (KeyboardInterrupt):
        pass
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    finally:
           # Cleanup
        stream.stop_stream()
        stream.close()
        p.terminate()
        sys.exit(0)
    sys.exit(-1)


if __name__ == '__main__':
    virtualTheremin()
