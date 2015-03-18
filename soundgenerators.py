'''Sound Makers'''
import warnings
import numpy as np
tau = 2 * np.pi
import scipy.signal
from main import fs, chunkSize


'''Waveform Functions'''
sin      = np.sin
square   = scipy.signal.square
sawtooth = scipy.signal.sawtooth
def triangle(*args, **kwargs):
    return scipy.signal.sawtooth(*args, width=0.5, **kwargs)


'''Sound Generators'''
class Osc(object):
    '''Simple Oscillator
    
    Properties:
        - frequency:    Oscillation Frequency
        - waveformFunc: Function for waveform. sin, triangle, square, sawtooth
    '''
    def __init__(self, frequency=220, waveformFunc=sin):
        self.frequency = frequency
        self.waveformFunc = waveformFunc
        self.__phase = 0


    def read(self):
        tEnd = chunkSize / float(fs)
        ts = np.arange(0, tEnd, 1. / fs)
        signal = self.waveformFunc(tau * self.frequency * ts + self.__phase)
        self.__phase = (tau * self.frequency * tEnd + self.__phase) % tau
        return signal


class FMOsc(Osc):
    '''Frequency Modulated (FM) Oscillator
    
    Properties:
        - frequency:    Oscillation Frequency
        - waveformFunc: Function for waveform. sin, triangle, square, sawtooth
        - fmFrequency:  Frequency of the Frequency Modulation (FM)
        - fmAmount:     Intensity of the Frequency Modulation (FM)
    '''
    def __init__(self, frequency=220, waveformFunc=sin, fmFrequency=5, fmAmount=5):
        super(FMOsc, self).__init__(frequency, waveformFunc)
        self.fmAmount = fmAmount
        self.__lfo = Osc(fmFrequency)


    def read(self):
        tEnd = chunkSize / float(fs)
        ts = np.arange(0, tEnd, 1. / fs)
        freqs = self.frequency + self.fmAmount * self.__lfo.read()
        signal = self.waveformFunc(tau * freqs * ts + self._Osc__phase)
        self._Osc__phase = (tau * freqs[-1] * tEnd + self._Osc__phase) % tau
        return signal


    @property
    def fmFrequency(self):
        return self._FMOsc__lfo.frequency

    @fmFrequency.setter
    def fmFrequency(self, freq):
        self._FMOsc__lfo.frequency = freq


class Theremin(object):
    '''Virtual Theremin. Mixes sounds from two oscillators and uses a third for
    Amplitude Modulation.

    Properties:
        - frequency:        Oscillation Frequency
        - waveformFunc1:    Waveform function for the first Oscillator (osc1).
                            E.g. sin, triangle, square, sawtooth
        - waveformFunc2:    Waveform function for the second Oscillator (osc2).
                            E.g. sin, triangle, square, sawtooth
        - vibratoFrequency: Frequency of the Vibrato Effect.
        - vibratoAmount:    Intensity of the Vibrato Effect.
        - tremoloFrequency: Frequency of Tremolo Effect
        - tremoloAmount:    Intensity of Tremolo Effect. (values in [0.0, 1.0])
        - volume:           Volume of sound. (values in [0.0, 1.0])
        - morph:            Mix paramter of osc1 and osc2. (values in [0.0, 1.0])
    '''
    def __init__(self, frequency=220, waveformFunc1=sin, waveformFunc2=square,
            vibratoFrequency=5, vibratoAmount=0, tremoloFrequency=8,
            tremoloAmount=0):
        self.__osc1 = FMOsc(frequency, waveformFunc1, vibratoFrequency, vibratoAmount)
        self.__osc2 = FMOsc(frequency, waveformFunc2, vibratoFrequency, vibratoAmount)
        self.__lfo = Osc(tremoloFrequency)
        self.__tremoloAmount = tremoloAmount
        self.__volume = 1.0
        self.__morph = 0.0


    def read(self):
        osc1Signal = self.__osc1.read()
        osc2Signal = self.__osc2.read()
        signal = (1.0 - self._Theremin__morph) * osc1Signal + self._Theremin__morph * osc2Signal
        lfoSignal = self.__lfo.read()
        return self.__volume * signal * (1. + .5 * self.__tremoloAmount * (lfoSignal - 1))


    '''frequency'''
    @property
    def frequency(self):
        return self._Theremin__osc1.frequency

    @frequency.setter
    def frequency(self, freq):
        self._Theremin__osc1.frequency = freq
        self._Theremin__osc2.frequency = freq


    '''waveform'''
    @property
    def waveformFunc1(self):
        return self._Theremin__osc1.waveformFunc

    @waveformFunc1.setter
    def waveformFunc1(self, func):
        self._Theremin__osc1.waveformFunc = func

    @property
    def waveformFunc(self):
        return self._Theremin__osc1.waveformFunc

    @waveformFunc.setter
    def waveformFunc(self, func):
        self._Theremin__osc1.waveformFunc = func

    @property
    def waveformFunc2(self):
        return self._Theremin__osc2.waveformFunc

    @waveformFunc2.setter
    def waveformFunc1(self, func):
        self._Theremin__osc2.waveformFunc = func


    '''vibratoFrequency'''
    @property
    def vibratoFrequency(self):
        return self._Theremin__osc1.fmFrequency

    @vibratoFrequency.setter
    def vibratoFrequency(self, freq):
        self._Theremin__osc1.fmFrequency = freq
        self._Theremin__osc2.fmFrequency = freq


    '''vibratoAmount'''
    @property
    def vibratoAmount(self):
        return self._Theremin__osc1.fmAmount

    @vibratoAmount.setter
    def vibratoAmount(self, amount):
        self._Theremin__osc1.fmAmount = amount
        self._Theremin__osc2.fmAmount = amount


    '''tremoloFrequency'''
    @property
    def tremoloFrequency(self):
        return self._Theremin__lfo.frequency

    @tremoloFrequency.setter
    def tremoloFrequency(self, freq):
        self._Theremin__lfo.frequency = freq


    '''tremoloAmount'''
    @property
    def tremoloAmount(self):
        return self._Theremin__tremoloAmount

    @tremoloAmount.setter
    def tremoloAmount(self, val):
        if 0.0 <= val <= 1.0:
            self._Theremin__tremoloAmount = val
        else:
            warnings.warn('No legit value for tremoloAmount')


    '''volume'''
    @property
    def volume(self):
        return self._Theremin__volume

    @volume.setter
    def volume(self, val):
        if 0.0 <= val <= 1.0:
            self._Theremin__volume = val
        else:
            warnings.warn('No legit value for volume')


    '''morph'''
    @property
    def morph(self):
        return self._Theremin__morph

    @morph.setter
    def morph(self, val):
        if 0.0 <= val <= 1.0:
            self._Theremin__morph = val
        else:
            warnings.warn('No legit value for morph')
