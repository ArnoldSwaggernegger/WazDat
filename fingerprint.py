import numpy as np
import matplotlib.pyplot as plt


def get_fingerprints(signal):
    '''
    get spectrogram peaks as (time, frequency) points
    '''

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
        result.append((frequencies, np.abs(spectrum)))
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
    frequencies0, _ = spectogram[0]
    width = len(spectogram)
    height = len(frequencies0)

    image = np.empty((width, height))
    for x in xrange(width):
        _, spectrum = spectogram[x]
        image[x] = spectrum

    plt.imshow(image.T, aspect="auto", extent=[0, time, frequencies0[0], frequencies0[-1]])
    ax = plt.gca()
    ax.set_xlabel("Time")
    ax.set_ylabel("Frequencies")
    plt.show()

if __name__ == "__main__":
    import soundfiles
    signal = soundfiles.load_wav("audio/ijsvogel.wav")
    spectogram = get_spectogram(signal, 800)
    """for sample in spectogram[:3]:
        (freqs, spectrum) = sample
        plt.plot(freqs, spectrum)
        plt.show()"""
    show_spectogram(spectogram, 1.0 * len(signal.get_samples()) / signal.get_samplerate())
