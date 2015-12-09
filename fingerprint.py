""" 
    fingerprint.py
"""


import numpy as np

import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
from scipy.io.wavfile import read

import classifier


def get_tokens(signal, window_size=2048, bin_size=8):
    fingerprints = get_fingerprints(signal, window_size, bin_size)
    result = []

    leftoffset = 1
    width = 4
    height = 16
    
    for time, peaks in fingerprints:
        realtime = time * float(window_size) / signal.get_samplerate()
        for anchorpoint in peaks:
            minfreq = anchorpoint - height / 2
            maxfreq = anchorpoint + height / 2
            for searchtime in xrange(time + leftoffset, min(time + leftoffset + width, len(fingerprints))):
                for matchpoint in fingerprints[searchtime][1]:
                    if minfreq <= matchpoint <= maxfreq:
                        result.append(classifier.Token((anchorpoint, matchpoint, searchtime - time), realtime, signal.get_filename()))

    return result


def get_fingerprints(signal, window_size, bin_size):
    '''
    get spectrogram peaks as (time, frequency) points
    '''

    result = []
    time_samples = get_spectogram(signal, window_size, bin_size)
    #show_spectogram(time_samples)

    width = time_samples.shape[1]
    #prev_histogram = np.zeros(width)
    for time, histogram in enumerate(time_samples):
        peaks = get_peaks(histogram)
        result.append((time, peaks))
        
        #TODO: Implement something like in the 3rd article with a guassian blur at peaks
        #prev_histogram = histogram

    return result


def get_peaks(histogram):
    '''
    Returns the peaks for a given amplitude plot.
    '''
    location_peaks = argrelextrema(np.array(histogram), np.greater)[0]
    peaks = [(i, histogram[i]) for i in location_peaks]
    peaks = sorted(peaks, key=lambda pair: pair[1], reverse=True)

    result = []
    for peak in peaks[:5]:
        if peak[1] > 150:
            result.append(peak[0])
    return result
    #return [peak[0] for peak in peaks[:5]]


def get_spectogram(signal, window_size, bin_size):
    '''
    '''
    samples = signal.get_samples()
    width = len(samples) / window_size
    height = window_size / 2 / bin_size
    window = zero_padded_window(window_size)

    result = np.empty((width, height))

    highpass_filter = np.zeros(height)
    cutoff_frequency = 100
    slope = 20
    for i in xrange(cutoff_frequency):
        highpass_filter[i] = 1.

    for t in range(0, width):
        partial_signal = window * samples[t*window_size:(t+1)*window_size]
        spectrum = np.fft.rfft(partial_signal)

        for bin in xrange(height):
            sum = 0.0
            for offset in xrange(bin_size):
                sum += np.abs(spectrum[bin*bin_size+offset])
            result[t][height-bin-1] = sum * highpass_filter[height-bin-1]

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
    #plt.show()


if __name__ == "__main__":
    import soundfiles
    
    signal = soundfiles.load_wav("training/pokemon/003.wav")

    x = []
    for i in signal:
        x.append(i)

    plt.subplot(411)
    plt.title("original")
    plt.plot(x)

    '''
    fingers =  get_fingerprints(signal, 2048, 8)
    time = []
    peaks = []
    
    for t, ps in fingers:
        time  += [t] * len(ps)
        peaks += ps

    plt.subplot(221)
    plt.title("original")
    plt.scatter(time, peaks, color="red")
    '''

    signal = soundfiles.load_wav("audio/pokemon/003-divided.wav")

    x = []
    for i in signal:
        x.append(i)

    plt.subplot(412)
    plt.title("divided")
    plt.plot(x)
    
    '''
    fingers =  get_fingerprints(signal, 2048, 8)
    time = []
    peaks = []

    for t, ps in fingers:
        time  += [t] * len(ps)
        peaks += ps

    plt.subplot(222)
    plt.title("amplified")
    plt.scatter(time, peaks, color="red")
    '''

    signal = soundfiles.load_wav("audio/pokemon/003-translated.wav")

    x = []
    for i in signal:
        x.append(i)

    plt.subplot(413)
    plt.title("offset")
    plt.xlim(20480,40480)
    plt.plot(x)
    
    '''
    fingers =  get_fingerprints(signal, 2048, 8)
    time = []
    peaks = []

    for t, ps in fingers:
        time  += [t] * len(ps)
        peaks += ps

    plt.subplot(223)
    plt.title("offset")
    plt.scatter(time, peaks, color="red")
    '''

    signal = soundfiles.load_wav("audio/pokemon/003-noise.wav")

    x = []
    for i in signal:
        x.append(i)

    plt.subplot(414)
    plt.title("noise")
    plt.plot(x)
    plt.show()
    
    '''
    fingers =  get_fingerprints(signal, 2048, 8)
    time = []
    peaks = []

    for t, ps in fingers:
        time  += [t] * len(ps)
        peaks += ps

    
    plt.subplot(224)
    plt.title("noise")
    plt.scatter(time, peaks, color="red")
    plt.show()
    '''
