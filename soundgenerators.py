'''Sound Generators'''
import warnings
import numpy as np
import scipy.signal
import config
tau = 2 * np.pi


'''Waveform Functions'''
sin = np.sin
sawtooth = scipy.signal.sawtooth
square = scipy.signal.square


def triangle(*args, **kwargs):
    return scipy.signal.sawtooth(*args, width=0.5, **kwargs)


'''Sound Generators'''


class Osc(object):
    '''Simple Oscillator

    Attributes/Properies:
        - frequency:     Oscillation frequency
        - waveform_func: Function for signal generation
    '''
    def __init__(self, frequency=220, waveform_func=sin):
        self.frequency = frequency
        self.waveform_func = waveform_func
        self._phase = 0.

    def read(self):
        tEnd = config.chunkSize / float(config.fs)
        ts = np.arange(0, tEnd, 1. / config.fs)
        signal = self.waveform_func(tau * self.frequency * ts + self._phase)
        self._phase = (tau * self.frequency * tEnd + self._phase) % tau
        return signal

    def __repr__(self):
        txt = 'Osc(frequency: {:.2f} Hz, waveform_func: {})'
        return txt.format(self.frequency,
                          self.waveform_func.__name__)


class FMOsc(Osc):
    '''Frequency Modulated (FM) Oscillator

    Attributes/Properies:
        - frequency:     Oscillation frequency
        - waveform_func: Function for signal generation
        - fmFrequency:   Frequency of the frequency modulation (FM)
        - fmAmount:      Intensity of the frequency modulation (FM)
    '''
    def __init__(self, frequency=220, waveform_func=sin, fmFrequency=5,
                 fmAmount=10):
        super(FMOsc, self).__init__(frequency, waveform_func)
        self.fmAmount = fmAmount
        self._lfo = Osc(fmFrequency)

    def read(self):
        tEnd = config.chunkSize / float(config.fs)
        ts = np.arange(0, tEnd, 1. / config.fs)
        freqs = self.frequency + self.fmAmount * self._lfo.read()
        signal = self.waveform_func(tau * freqs * ts + self._phase)
        self._phase = (tau * freqs[-1] * tEnd + self._phase) % tau
        return signal

    @property
    def fmFrequency(self):
        return self._lfo.frequency

    @fmFrequency.setter
    def fmFrequency(self, freq):
        self._lfo.frequency = freq

    def __repr__(self):
        txt = ('FMOsc(frequency: {:.2f} Hz, '
               'waveform_func: {}, '
               'fmFrequency: {:.2f} Hz, '
               'fmAmount: {:.2f} Hz)')

        return txt.format(self.frequency,
                          self.waveform_func.__name__,
                          self._lfo.frequency,
                          self.fmAmount)


class Theremin(object):
    '''Theremin

    One signal oscillators (FMOsc) and one lfo-oscillators for Amplitude
    Modulation.

    Attributes/Properies:
        - frequency:        Signal oscillators frequency
        - volume:           Volume of sound (values in [0.0, 1.0])
        - waveform_func:    Function for signal generation (sin, triangle,
                            square, sawtooth)
        - vibratoFrequency: Frequency of the vibrato effect
        - vibratoAmount:    Intensity of the vibrato effect
        - tremoloFrequency: Frequency of tremolo effect
        - tremoloAmount:    Intensity of tremolo effect (values in [0.0, 1.0])
    '''
    def __init__(self, frequency=220, waveform_func=sin, vibratoFrequency=5,
                 vibratoAmount=0, tremoloFrequency=8, tremoloAmount=0):
        self._fmOsc = FMOsc(frequency, waveform_func, vibratoFrequency,
                            vibratoAmount)
        self._lfo = Osc(tremoloFrequency)
        self._tremoloAmount = tremoloAmount
        self._volume = 1.0

    def read(self):
        fmOscSignal = self._fmOsc.read()
        lfoSignal = self._lfo.read()
        signal = fmOscSignal * (1. + .5 * self._tremoloAmount * (lfoSignal - 1.))
        return self._volume * signal

    '''Frequency'''
    @property
    def frequency(self):
        return self._fmOsc.frequency

    @frequency.setter
    def frequency(self, freq):
        self._fmOsc.frequency = freq

    '''Volume'''
    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, val):
        if val < 0 or 1 < val:
            warnings.warn('%d No legit value for volume' % val)
        self._volume = max(0., min(1., val))

    '''Waveform'''
    @property
    def waveform_func(self):
        return self._fmOsc.waveform_func

    @waveform_func.setter
    def waveform_func(self, func):
        self._fmOsc.waveform_func = func

    '''Vibrato Frequency'''
    @property
    def vibratoFrequency(self):
        return self._fmOsc.fmFrequency

    @vibratoFrequency.setter
    def vibratoFrequency(self, freq):
        self._fmOsc.fmFrequency = freq

    '''Vibrato Amount'''
    @property
    def vibratoAmount(self):
        return self._fmOsc.fmAmount

    @vibratoAmount.setter
    def vibratoAmount(self, amount):
        self._fmOsc.fmAmount = amount

    '''Tremolo Frequency'''
    @property
    def tremoloFrequency(self):
        return self._lfo.frequency

    @tremoloFrequency.setter
    def tremoloFrequency(self, freq):
        self._lfo.frequency = freq

    '''Tremolo Amount'''
    @property
    def tremoloAmount(self):
        return self._tremoloAmount

    @tremoloAmount.setter
    def tremoloAmount(self, val):
        if val < 0 or 1 < val:
            warnings.warn('%d No legit value for tremoloAmount' % val)
        self._tremoloAmount = max(0., min(1., val))

    def __repr__(self):
        txt = ('Theremin(frequency: {:.2f} Hz, '
               'volume: {:.1f}, '
               'waveform_func: {}, '
               'vibratoFrequency: {:.2f} Hz, '
               'vibratoAmount: {:.1f}, '
               'tremoloFrequency: {:.2f} Hz, '
               'tremoloAmount: {:.1f})')

        return txt.format(self.frequency,
                          self.volume,
                          self.waveform_func.__name__,
                          self.vibratoFrequency,
                          self.vibratoAmount,
                          self.tremoloFrequency,
                          self.tremoloAmount)


'''Testing Properies'''
if __name__ == '__main__':
    # Testing Osc
    osc = Osc()
    osc.frequency = 1
    osc.frequency
    osc.waveform_func = triangle
    osc.waveform_func
    print osc
    osc.read()

    # Testing FMOsc
    fmOsc = FMOsc()
    fmOsc.frequency = 1
    fmOsc.frequency
    fmOsc.waveform_func = triangle
    fmOsc.waveform_func
    fmOsc.fmFrequency = 2
    fmOsc.fmFrequency
    fmOsc.fmAmount = 3
    fmOsc.fmAmount
    print fmOsc
    fmOsc.read()

    # Testing Theremin
    theremin = Theremin()
    theremin.frequency = 1
    theremin.frequency
    theremin.volume = 0.3
    theremin.volume
    theremin.waveform_func = triangle
    theremin.waveform_func
    theremin.vibratoFrequency = 2
    theremin.vibratoFrequency
    theremin.vibratoAmount = 3
    theremin.vibratoAmount
    theremin.tremoloFrequency = 4
    theremin.tremoloFrequency
    theremin.tremoloAmount = 0.7
    theremin.tremoloAmount
    print theremin
    theremin.read()
