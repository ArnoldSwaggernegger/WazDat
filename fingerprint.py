import numpy as np


def get_fingerprints(signal, window_size=100):
    '''
    get spectrogram peaks as (time, frequency) points
    '''

    samples = signal.get_samples()

    for i in range(0, samples.length, window_size):
        window = zero_padded_window(len(samples), i, window_size)
        partial_signal = window * samples
        spectrum = np.fft.fft(partial_signal)
        frequencies = np.fft.fftfreq(len(spectrum))


def zero_padded_window(length, index, size):
    '''
    '''
    window = np.zeros(length)
    window[index:index + size] = 1
    return window


def hanning_window(length, index, size):
    '''
    '''
    return None


def hamming_window(length, index, size):
    '''
    '''
    return None
