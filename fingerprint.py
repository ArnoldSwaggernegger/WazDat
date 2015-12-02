import numpy as np
import matplotlib.pyplot as plt


def get_fingerprints(signal):
    '''
    get spectrogram peaks as (time, frequency) points
    '''

def get_keypoints(spectogram):


def get_spectogram(signal, window_size):
    result = []
    samples = signal.get_samples()
    for i in range(0, len(samples), window_size):
        r = min(len(samples), i + window_size)
        window = zero_padded_window(r - i)
        partial_signal = window * samples[i:r]
        spectrum = np.fft.rfft(partial_signal)
        frequencies = np.fft.rfftfreq(
            len(partial_signal), 1.0 / signal.get_samplerate()
        )
        result.append((frequencies, np.abs(spectrum)))
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

if __name__ == "__main__":
    import soundfiles
    signal = soundfiles.load_wav("test/muziek.wav")
    spectogram = get_spectogram(signal, 800)
    for sample in spectogram[:3]:
        (freqs, spectrum) = sample
        plt.plot(freqs, spectrum)
        plt.show()
