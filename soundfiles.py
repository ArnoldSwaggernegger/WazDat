"""
    This class provides a wrapper around signals from sound files. We cannot
    work well with just ndarrays as sound signals. 
"""


from glob import glob


""" Returns all matching filenames. 
    Example: expression = "data/*" find all files inside the folder data. """
def find_files(expression):
    return glob(expression)


""" Load a file as an array of samples. """
def load_signal(filename):
    
    # load signal as numpy-ndarray
    # for multiple filetypes (mp3, wav etc) 
    
    # create Signal object   

    return None


class Signal():
    
    filename = ""
    
    def __init__(self, samples, samplerate):
        self.samples = samples
        self.samplerate = samplerate

    """ Getters. """

    def get_samplerate(self):
        return self.samplerate
        
    def get_duration(self):
        return self.samplerate * len(self.samples)
     
    def get_filename(self):
        return self.filename
     
    def set_filename(self, filename):
        self.filename = filename
     
    """ Implement some basic array operators. """
        
    def __getitem__(self, index):
        return self.samples[index]
        
    def __len__(self):
        return len(self.samples)
