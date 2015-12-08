'''
soundfiles.py

This file contains function to load audio files into Signal objects
containing raw samples.
'''


import numpy as np

from glob import glob
from wave import open
from os.path import isfile
from scikits.samplerate import resample


def find_files(expression):
    '''
    This function returns all matching filenames.
    Example: expression = "data/*" find all files inside the folder data.
    '''
    return glob(expression)


def load_signal(filename):
    '''
    This function reads a file and creates a Signal object containing the
    samples.
    '''

    if not isfile(filename):
        print "Error: file not found"
        return None

    if ".wav" in filename:
        return load_wav(filename)

    if ".mp3" in filename:
        return load_mp3(filename)

    if ".ogg" in filename:
        return load_ogg(filename)

    print "Error: filetype not supported"
    return None


def load_wav(filename):
    '''
    '''
    f = open(filename, "r")

    nchannels, samplewidth, framerate, nframes,\
        _, _ = f.getparams()
    frames = f.readframes(nframes)
    f.close()

    if samplewidth == 1:
        dtype = np.int8
        maxvalue = 2 ** (8 - 1)
    elif samplewidth == 2:
        dtype = np.int16
        maxvalue = 2 ** (16 - 1)
    elif samplewidth == 4:
        dtype = np.int32
        maxvalue = 2 ** (32 - 1)
    else:
        print "Error: unsupported samplewidth {}".format(samplewidth)
        return None

    all_samples = np.fromstring(frames, dtype)

    combined_samples = np.zeros(nframes)

    for i in xrange(nchannels):
        a = combined_samples
        b = all_samples[i::nchannels]
        condition = np.less(np.abs(a), np.abs(b))
        combined_samples = np.choose(condition, [a, b])

    normalized_samples = combined_samples / maxvalue

    desired_framerate = 16000.
    resampled_samples = resample(normalized_samples,
                                 desired_framerate / framerate, 'sinc_best')

    return Signal(resampled_samples, desired_framerate, filename)


def load_mp3(filename):
    return None


def load_ogg(filename):
    return None


class Signal():
    '''
    This class provides a wrapper around signals from sound files. We cannot
    work well with just ndarrays as sound signals, as the time at which the
    peak occur are related to the samplerate.
    '''

    def __init__(self, samples, samplerate, filename):
        self.samples = samples
        self.samplerate = samplerate
        self.filename = filename

    def get_samples(self):
        return self.samples

    def get_samplerate(self):
        return self.samplerate

    def get_duration(self):
        return len(self.samples) / float(self.samplerate)

    def get_filename(self):
        return self.filename

    def __getitem__(self, index):
        return self.samples[index]

    def __len__(self):
        return len(self.samples)
