import numpy as np
import matplotlib.pyplot as plt


def get_fingerprints(signal, window_size=8000):
    '''
    get spectrogram peaks as (time, frequency) points
    '''

    samples = signal.get_samples()

    for i in range(0, len(samples), window_size):
        r = min(len(samples), i + window_size)
        window = zero_padded_window(r - i)
        partial_signal = window * samples[i:r]
        spectrum = np.fft.rfft(partial_signal)
        frequencies = np.fft.rfftfreq(
            len(partial_signal), 1.0 / signal.get_samplerate()
        )

        get_peaks()


def get_peaks():
    '''
    '''
    pass


def zero_padded_window(size):
    '''
    '''
    return np.ones(size)


def hanning_window(length, index, size):
    '''
    '''
    return None


def hamming_window(length, index, size):
    '''
    '''
    return None
