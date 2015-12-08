'''
The classifier uses a hashtable based on fingerprint hashes.
For each possible matched file, check whether the time points between the
hashes are more or less the same.
'''


import numpy as np


FREQUENCY_MARGIN = 4


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

    def as_dict(self):
        return {
            'fingerprint': self.fingerprint,
            'time': self.time,
            'filename': self.filename
        }

    def __str__(self):
        return "({} {} {})".format(self.fingerprint, self.time, self.filename)


class Classifier:

    def __init__(self):
        self.tokens = {}

    def add_token(self, token):
    
        p1, _, _ = token.fingerprint
    
        if p1 in self.tokens:
            self.tokens[p1].append(token)
        else:
            self.tokens[p1] = [token]

    def classify(self, tokens):

        '''
        This function classifies a sound using the collected tokens.
        The input tokens should all belong to the same file.
        '''

        matches = []

        ''' Find all matches between input tokens and database tokens. '''
        # TODO: this part can be sped up using a hashtable-like ordening of
        # the collected tokens

        for b in tokens:
        
            b1, b2, _ = b.fingerprint
        
            for index in xrange(b1 - FREQUENCY_MARGIN, b1 + FREQUENCY_MARGIN + 1):
                
                if not index in self.tokens:
                    continue
                
                subset = self.tokens[index]
                
                for a in subset:
                
                    a1, a2, _ = a.fingerprint
            
                    if -FREQUENCY_MARGIN <= a2 - b2 <= +FREQUENCY_MARGIN:
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
             
            """ Create a histogram with binsize 0.5. The two additional bins at 
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
