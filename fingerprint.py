import numpy as np
import matplotlib.pyplot as plt


def get_fingerprints(signal):
    '''
    get spectrogram peaks as (time, frequency) points
    '''

def get_spectogram(signal, window_size, bin_size):
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
            result[t][bin] = sum

    return result

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

def show_spectogram(spectogram, time):
    plt.imshow(spectogram.T, aspect="auto")
    ax = plt.gca()
    ax.set_xlabel("Time")
    ax.set_ylabel("Frequencies")
    plt.show()

if __name__ == "__main__":
    import soundfiles
    signal = soundfiles.load_wav("audio/gaai.wav")
    spectogram = get_spectogram(signal, 2048, 2)
    """for sample in spectogram[:3]:
        (freqs, spectrum) = sample
        plt.plot(freqs, spectrum)
        plt.show()"""
    show_spectogram(spectogram, 1.0 * len(signal.get_samples()) / signal.get_samplerate())
