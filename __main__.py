'''Virtual Theremin'''
import sys
import config
import pyaudio
import soundgenerators
import musicscale
from helpers import freq_2_note
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
    '''Print Theremin state infos'''
    freq = theremin.frequency
    vol = theremin.volume
    note = freq_2_note(freq)
    print 'Note: {0}, frequency: {1} Hz, volume: {2}'.format(note, freq, vol)


def lefthand(hand):
    '''Handler for left hand
    
    hand.pinch -> which musical scaling
    hand.palmState -> tremolo intensity
    y position -> volume
    '''
    global theremin, scaling_func # TODO: global could possibly be eliminated
    handState = leapprocessors.HandState(hand)
    print "Left : pinch=% d, palmState=%.2f" % (handState.pinch, handState.palmState)

    # Pinching Gesture
    p = handState.pinch
    if p != -1:
        scaling_func = [musicscale.no_scaling,
                        musicscale.scale_to_chroma,
                        musicscale.scale_to_major,
                        musicscale.scale_to_pentatonic][p]

    # Open/Closed Hand
    alpha = handState.palmState
    theremin.tremoloAmount = 1. - alpha

    # Position -> Vol
    __, y, __ = handState.palmPosition
    theremin.volume = y


def righthand(hand):
    '''handler for right hand
    
    hand.pinch -> waveform
    hand.palmState -> vibrato intensity
    z position -> frequency
    '''
    global theremin, scaling_func # TODO: global could possibly be eliminated
    handState = leapprocessors.HandState(hand)
    print "Right: pinch=% d, palmState=%.2f" % (handState.pinch, handState.palmState)

    # Pinching Gesture
    p = handState.pinch
    if p != -1:
        theremin.waveform_func = [soundgenerators.sin,
                                  soundgenerators.triangle,
                                  soundgenerators.sawtooth,
                                  soundgenerators.square][p]

    # Open/Closed Hand
    alpha = handState.palmState
    theremin.vibratoAmount = (1. - alpha) * 10

    # Position -> freq
    __, __, z = handState.palmPosition
    freq = config.fmin + (1. - z) * config.fmax
    theremin.frequency = scaling_func(freq)


def virtual_theremin():
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
        # Exit
        stream.stop_stream()
        stream.close()
        p.terminate()
        sys.exit(0)

    sys.exit(-1)


if __name__ == '__main__':
    virtual_theremin()
