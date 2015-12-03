import numpy as np
import matplotlib.pyplot as plt


def get_fingerprints(signal):
    '''
    get spectrogram peaks as (time, frequency) points
    '''


def get_spectogram(signal, window_s):
    '''
    '''
    samples = signal.get_samples()
    width = len(samples) / window_s
    height = window_s / 2
    window = zero_padded_window(window_s)

    result = np.empty((width, height))
    for t in range(0, width):
        partial_signal = window * samples[t * window_s:(t + 1) * window_s]
        spectrum = np.fft.rfft(partial_signal)[:height]
        result[t] = np.abs(spectrum)

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
    '''
    '''
    plt.imshow(spectogram.T, aspect="auto")
    ax = plt.gca()
    ax.set_xlabel("Time")
    ax.set_ylabel("Frequencies")
    plt.show()

if __name__ == "__main__":
    '''
    '''
    import soundfiles
    signal = soundfiles.load_wav("audio/gaai.wav")
    spectogram = get_spectogram(signal, 1024)
    '''for sample in spectogram[:3]:
        (freqs, spectrum) = sample
        plt.plot(freqs, spectrum)
        plt.show()'''
    show_spectogram(
        spectogram,
        1.0 * len(signal.get_samples()) / signal.get_samplerate()
    )
