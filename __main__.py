'''Virtual Theremin'''
import sys
import config
import pyaudio
import soundgenerators
import musicscale
import helpers

helpers.addLeapPath()
#import Leap, leapprocessors
import leapprocessors


# Init
theremin = soundgenerators.Theremin()
theremin.volume = 0.4
theremin.frequency = config.fmin
scaling_func = musicscale.no_scaling

def printInfo(theremin):
    print helpers.freqency_to_note(theremin.frequency), " Freq = ", theremin.frequency, ", Volume =", theremin.volume
    #print helpers.freqency_to_note(theremin.frequency)


def lefthand(hand):
    '''Handler for left hand'''
    global theremin, scaling_func
    handState = leapprocessors.HandState(hand)
    print "Left  ", handState.Pinch, handState.PalmState

    # Pinching Gesture
    p = handState.Pinch
    if p != -1:
        scaling_func = [musicscale.no_scaling,
                        musicscale.scale_to_chroma,
                        musicscale.scale_to_major,
                        musicscale.scale_to_pentatonic][p]

    # Open/Closed Hand
    alpha = handState.PalmState
    theremin.tremoloAmount = 1. - alpha

    # Position -> Vol
    __, y, __ = handState.PalmPosition
    theremin.volume = y
    

def righthand(hand):
    '''handler for right hand'''
    global theremin, scaling_func
    handState = leapprocessors.HandState(hand)
    print "Right ", handState.Pinch, handState.PalmState

    # Pinching Gesture
    p = handState.Pinch
    if p != -1:
        theremin._Theremin__osc1.waveformFunc = [soundgenerators.sin,
                                                 soundgenerators.triangle, 
                                                 soundgenerators.sawtooth,
                                                 soundgenerators.square][p]

    # Open/Closed Hand
    alpha = handState.PalmState
    theremin.vibratoAmount = (1. - alpha) * 10
    
    # Position -> freq
    __, __, z = handState.PalmPosition
    freq = config.fmin + (1. - z) * config.fmax
    theremin.frequency = scaling_func(freq)

    

def virtualTheremin(): 
    try:
        # Init PyAudio
        p = pyaudio.PyAudio()

        # Open up output stream
        stream = p.open(format=p.get_format_from_width(config.sampleWidth),
                        channels=config.nChannels,
                        rate=config.fs,
                        output=True)

        # Init Leap
        print "Initializing Leap"
        handProcessor = leapprocessors.HandProcessor()
        print "Done"

        # Attach handlers to left and right hand events
        handProcessor.attach_left_event_handler(lefthand)
        handProcessor.attach_right_event_handler(righthand)
        handProcessor.run()

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
