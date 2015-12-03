import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema


def get_fingerprints(signal, window_size):
    '''
    get spectrogram peaks as (time, frequency) points
    '''

    result = []
    time_samples = get_spectogram(signal, window_size)

    for time, frequencies, spectrum in time_samples:
        result.append((time, get_peaks(frequencies, spectrum)))

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

        result.append((i * signal.get_duration() / float(window_size), frequencies, np.abs(spectrum)))

    return result

def get_peaks(frequencies, magnitudes):
    '''
    Returns the peaks for a given amplitude plot.
    '''

    location_peaks = argrelextrema(np.array(magnitudes), np.greater)[0]
    peaks = [(frequencies[i], magnitudes[i]) for i in location_peaks]
    peaks = sorted(peaks, key=lambda pair: pair[1], reverse=True)

    return [peak[0] for peak in peaks[:5]]

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

def show_spectogram(spectogram, time):
    frequencies0, _ = spectogram[0]
    width = len(spectogram)
    height = len(frequencies0)
    print width, height

    image = np.empty((width, height))
    for x in xrange(width):
        _, spectrum = spectogram[x]
        image[x] = spectrum

    plt.imshow(image.T, cmap=plt.cm.Reds, aspect="auto", extent=[0, time, frequencies0[0], frequencies0[-1]])
    ax = plt.gca()
    ax.set_xlabel("Time")
    ax.set_ylabel("Frequencies")
    plt.show()

if __name__ == "__main__":
    print get_peaks([100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110], [1,2,1,3,1,4,1,5,1,6,1])
    import soundfiles
    signal = soundfiles.load_wav("audio/gaai.wav")
    spectogram = get_spectogram(signal, 800)

    n = signal.get_samples()
    fft = np.fft.fft(n)
    freqs =  np.fft.fftfreq(len(n), 1.0 / signal.get_samplerate())
    plt.plot(freqs, np.abs(fft))
    plt.show()
    """
    for sample in spectogram[:3]:
        (freqs, spectrum) = sample
        plt.plot(freqs, spectrum)
        plt.show()
    show_spectogram(spectogram, 1.0 * len(signal.get_samples()) / signal.get_samplerate())
    """

    fingers =  get_fingerprints(signal, 1024)
    time = []
    peaks = []
    for t, ps in fingers:
        time  += [t] * len(ps)
        peaks += ps
    plt.scatter(time, peaks)
    plt.show()
