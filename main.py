'''Virtual Theremin'''
from settings import *
import sys
import pyaudio
import soundgenerators
import helpers

helpers.addLeapPath()
import Leap, HandProcessor

def printInfo(theremin):
    print helpers.freqency_to_note(theremin.frequency), " Freq = ", theremin.frequency, ", Volume =", theremin.volume
    #print helpers.freqency_to_note(theremin.frequency)

# Handler for left hand
def lefthand(hand):
    handState = HandProcessor.HandState(hand)
    
    print handState.find

# Handler for right hand
def righthand(hand):
    handState = HandProcessor.HandState(hand)
    #print handState.Pinch
    print handState.PalmState


def virtualTheremin(): 
    try:
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
