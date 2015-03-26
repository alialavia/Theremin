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
    theremin.frequency = 220

    # Init Leap
    handprocessor = HandProcessor.HandProcessor()

    # set up event handlers for left hand and right hand
    def lefthand(hand):        
        
        normalized_palm = hand.frame.interaction_box.normalize_point(hand.palm_position)        
        theremin.volume = normalized_palm.y
        printInfo(theremin)

    def righthand(hand):

                     # 'C', 'C#', 'D',  'Eb', 'E',  'F', 'F#',  'G', 'G#','A',    'Bb', 'B'    'C'
        baseNotes = [
                     [261.6,    293.7,        329.6,349.2,      392.0,    440.0,        493.9, 523.3],
                     [261.6,277.2,293.7,311.1,329.6,349.2,370.0,392.0,415.3,440.0,466.2,493.9, 523.3]
                    ]

        normalized_palm = hand.frame.interaction_box.normalize_point(hand.palm_position)        
        pinch = helpers.findPinch(hand)

        currentScale = baseNotes[min(pinch+1, 1)]
        
        baseFreq = normalized_palm. z
        freqIndex = int((1.0-baseFreq) * len(currentScale) - 0.01)
        theremin.frequency = currentScale[freqIndex]
        printInfo(theremin)
        #print helpers.findPinch(hand)
        #print helpers.maxDistance(hand)

    def righthand_continous(hand):
        normalized_palm = hand.frame.interaction_box.normalize_point(hand.palm_position)
        theremin.frequency = 260.0 + (1.0 - normalized_palm.z) * 260.0
        printInfo(theremin)

    handprocessor.attachLeftEventHandler(lefthand)
    handprocessor.attachRightEventHandler(righthand_continous)
    handprocessor.run()

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
