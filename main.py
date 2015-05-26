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
fmin = 220. # [Hz]
fmax = 440. # [Hz]

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
    theremin.tremoloAmount = a

    # Position -> Vol
    x, y, z = handState.PalmPosition
    theremin.volume = y
    

# Handler for right hand
def righthand(hand):
    handState = HandProcessor.HandState(hand)
    global theremin, scaling_func

    # Pinching
    p = handState.Pinch
    if p != -1:
        if p == 0:
            theremin.waveFormFunc1 = soundgenerators.sin
        elif p == 1:
            theremin.waveFormFunc1 = soundgenerators.triangle
        elif p == 2:
            theremin.waveFormFunc1 = soundgenerators.sawtooth
        elif p == 3:
            theremin.waveFormFunc1 = soundgenerators.square
    
    # Open/Closed Hand
    a = handState.PalmState
    theremin.vibratoAmount = a
    
    # Position -> freq
    x, y, z = handState.PalmPosition
    freq = fmin + z * fmax
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
