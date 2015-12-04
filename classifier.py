'''
The classifier uses a hashtable based on fingerprint hashes.
For each possible matched file, check whether the time points between the
hashes are more or less the same.
'''


from random import random
import numpy as np


def similar(a, b):
    ''' 
    This function returns whether two tokens a and b have similar 
    fingerprint.
    '''
    # TODO not made for sound fingerprints, which should be tuples of (df, dt)
    if -0.1 <= a.fingerprint - b.fingerprint <= 0.1:
        return True
    return False 


def sort_per_filename(matches):
    ''' 
    This function sorts a list of tokens into a dictionary using the token
    filenames as keys and a list of the tokens from that filenames as 
    values. 
    ''' 
    d = {}
    for match in matches:
        a, b = match
        if a.filename in d:
            d[a.filename].append(match)    
        else:
            d[a.filename] = [match]          
    return d


class Token:

    ''' 
    The Token class is used to create token objects for the classifier.
    Each token contains the sound fingerprint, the corresponding time
    and the filename of the original file.
    '''
    
    def __init__(self, fingerprint, time, filename):
        self.fingerprint = fingerprint
        self.time = time
        self.filename = filename
        
    def __str__(self):
        return "({} {} {})".format(self.fingerprint, self.time, self.filename)


class Classifier:

    def __init__(self):    
        self.tokens = []
        
    def add_token(self, token):
        self.tokens.append(token)
        
    def classify(self, tokens):
    
        ''' 
        This function classifies a sound using the collected tokens.
        The input tokens should all belong to the same file.
        '''
        
        matches = []
             
        ''' Find all matches between input tokens and database tokens. '''
        # TODO: this part can be sped up using a hashtable-like ordening of
        # the collected tokens 
             
        for a in self.tokens:
             for b in tokens:
                if similar(a, b):
                    matches.append((a, b))
             
        ''' Sort all found matches based on original file. '''
        file_matches = sort_per_filename(matches)
             
        ''' Check each possible file match. If the candidate has a match for at 
            least 50% of the input tokens around the same time interval, it
            is very likely the correct match. '''
             
        for filename, matches in file_matches.iteritems():
        
            if len(matches) < 0.5 * len(tokens):
                continue
        
            dt = [a.time - b.time for match in matches]
            upper_bound = np.ceil(np.max(dt))
            lower_bound = np.floor(np.min(dt))
             
            """ Create a histogram with binsize 1. The two additional bins at 
                the edges are to make sure the next step always goes well. """
            binsize = 0.5
            histogram, bins = np.histogram(dt, bins=np.arange(lower_bound - binsize, upper_bound + 3 * binsize, binsize))
            
            """ If the highest peak in the histogram combined with its 
                neightbours cover at least 50% of the input tokens, this file
                is likely the good match. """
            maxindex = np.argmax(histogram)
            
            if histogram[maxindex - 1] + histogram[maxindex] + histogram[maxindex + 1] >= 0.5 * len(tokens):
                return filename

        return None
        
        
if __name__ == "__main__":

    cl = Classifier()
    
    a = [Token(i * np.sin(2 * i),  i, "a") for i in xrange(100)]
    b = [Token(i * np.sin(3 * i),  i, "b") for i in xrange(100)]
    c = [Token(i * np.sin(5 * i),  i, "c") for i in xrange(100)]
    d = [Token(i * np.sin(7 * i),  i, "d") for i in xrange(100)]
    e = [Token(i * np.sin(11 * i), i, "e") for i in xrange(100)]
    
    for i in a:
        cl.add_token(i)
    for i in b:
        cl.add_token(i)
    for i in c:
        cl.add_token(i)
    for i in d:
        cl.add_token(i)
    for i in e:
        cl.add_token(i)
    
    print cl.classify(a[20:30])
    print cl.classify(b[30:40])
    print cl.classify(c[40:50])
    print cl.classify(d[50:60])
    print cl.classify(e[70:80])
