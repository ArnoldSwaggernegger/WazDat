""" 
    fingerprint.py
"""


import numpy as np

import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
from scipy.io.wavfile import read

from classifier import Token


def get_tokens(signal, window_size=1024, bin_size=1):
    fingerprints = get_fingerprints(signal, window_size, bin_size)
    result = []

    leftoffset = 2
    width = 3
    height = 48
    for time, peaks in fingerprints:
        for anchorpoint in peaks:
            minfreq = anchorpoint - height / 2
            maxfreq = anchorpoint + height / 2
            for searchtime in xrange(time + leftoffset, min(time + leftoffset + width, len(fingerprints))):
                for matchpoint in fingerprints[searchtime][1]:
                    if minfreq <= matchpoint <= maxfreq:
                        result.append(Token((anchorpoint, matchpoint, searchtime - time), time, signal.get_filename()))

    return result


def get_fingerprints(signal, window_size=1024, bin_size=1):
    '''
    get spectrogram peaks as (time, frequency) points
    '''

    result = []
    time_samples = get_spectogram(signal, window_size, bin_size)

    #print time_samples
    for time, histogram in enumerate(time_samples):
        #print time, histogram
        result.append((time, get_peaks(histogram)))

    return result


def get_spectogram(signal, window_size):
    result = []
    samples = signal.get_samples()

    for i in range(0, len(samples)-window_size, window_size):
        window = zero_padded_window(window_size)
        partial_signal = window * samples[i:i+window_size]
        spectrum = np.fft.rfft(partial_signal)

        frequencies = np.fft.rfftfreq(
            len(partial_signal), 1.0 / signal.get_samplerate()
        )

        result.append((i * signal.get_duration() / float(window_size), frequencies, np.abs(spectgrum)))

    return result


def get_peaks(histogram):
    '''
    Returns the peaks for a given amplitude plot.
    '''
    location_peaks = argrelextrema(np.array(histogram), np.greater)[0]
    peaks = [(i, histogram[i]) for i in location_peaks]
    peaks = sorted(peaks, key=lambda pair: pair[1], reverse=True)

    return [peak[0] for peak in peaks[:5]]


def get_spectogram(signal, window_size, bin_size):
    '''
    '''
    samples = signal.get_samples()
    width = len(samples) / window_size
    height = window_size / 2 / bin_size
    window = zero_padded_window(window_size)

    result = np.empty((width, height))
    for t in range(0, width):
        partial_signal = window * samples[t*window_size:(t+1)*window_size]
        spectrum = np.fft.rfft(partial_signal)

        for bin in xrange(height):
            sum = 0.0
            for offset in xrange(bin_size):
                sum += np.abs(spectrum[bin*bin_size+offset])
            result[t][height-bin-1] = sum

    return result


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


def show_spectogram(spectogram):
    '''
    '''
    plt.imshow(spectogram.T, aspect="auto")
    ax = plt.gca()
    ax.set_xlabel("Time")
    ax.set_ylabel("Frequencies")
    plt.show()


if __name__ == "__main__":
    import soundfiles
    signal = soundfiles.load_wav("audio/muziek.wav")

    """
    for sample in spectogram[:3]:
        (freqs, spectrum) = sample
        plt.plot(freqs, spectrum)
        plt.show()
    show_spectogram(spectogram, 1.0 * len(signal.get_samples()) / signal.get_samplerate())
    """


    #fingers =  get_fingerprints(signal, 1024, 1)
    hashes = get_tokens(signal, 1024, 1)
    #print hashes
    """time = []
    peaks = []

    for t, ps in fingers:
        time  += [t] * len(ps)
        peaks += ps

    plt.scatter(time, peaks)
    plt.show()"""

