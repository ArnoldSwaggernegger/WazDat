"""
    This class provides a wrapper around signals from sound files. We cannot
    work well with just ndarrays as sound signals, as the time at which the
    peak occur are related to the samplerate.
"""


from glob import glob
from wave import open
import numpy as np


def find_files(expression):
    """ Returns all matching filenames. 
    Example: expression = "data/*" find all files inside the folder data. """
    return glob(expression)


def load_signal(filename):
    """ Load a file as an array of samples. """
    
    if ".wav" in filename:
        return load_wav(filename)
    
    if ".mp3" in filename:
        return load_mp3(filename)
        
    if ".ogg" in filename:
        return load_ogg(filename)
               
    return None
    
    
def load_wav(filename):    
    f = open(filename, "r")
    
    nchannels, samplewidth, framerate, nframes, comptype, compname = f.getparams()
    frames = f.readframes(nframes)
    f.close()
        
    if samplewidth == 2:
        dtype = np.int16
        maxvalue = 2 ** (16 - 1)
    if samplewidth == 4:
        dtype = np.int32
        maxvalue = 2 ** (32 - 1)
    
    all_samples = np.fromstring(frames, dtype)
    
    combined_samples = np.zeros(nframes)
    
    for i in xrange(nchannels):    
        a = combined_samples
        b = all_samples[i::nchannels]
        condition = np.less(np.abs(a), np.abs(b))
        combined_samples = np.choose(condition, [a, b])

    normalized_samples = combined_samples / maxvalue
    
    return Signal(normalized_samples, framerate)

    
def load_mp3(filename):  
    pass
    

def load_ogg(filename):
    pass


class Signal():
    
    def __init__(self, samples, samplerate):
        self.samples = samples
        self.samplerate = samplerate
        self.filename = ""

    def get_samples(self):
        return self.samples

    def get_samplerate(self):
        return self.samplerate
        
    def get_duration(self):
        return self.samplerate * len(self.samples)
     
    def get_filename(self):
        return self.filename
        
    def __getitem__(self, index):
        return self.samples[index]
        
    def __len__(self):
        return len(self.samples)
        
if __name__ == "__main__":

    signal = load_wav("test/muziek.wav")
    
    print signal.samplerate
    print signal.samples
