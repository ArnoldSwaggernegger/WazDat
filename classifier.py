'''
The classifier uses a hashtable based on fingerprint hashes.
For each possible matched file, check whether the time points between the
hashes are more or less the same.
'''


import numpy as np
import database as db
import matplotlib.pyplot as plt


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
        p1, p2, _ = token.fingerprint

        if p1 in self.tokens:
            if p2 in self.tokens[p1]:
                self.tokens[p1][p2].append(token)
            else:
                self.tokens[p1].update({p2: [token]})
        else:
            self.tokens[p1] = {p2: [token]}

    def classify(self, tokens):

        '''
        This function classifies a sound using the collected tokens.
        The input tokens should all belong to the same file.
        '''

        matches = []

        ''' Find all matches between input tokens and database tokens. '''

        for b in tokens:
            b1, b2, b3 = b.fingerprint
            if b1 in self.tokens and b2 in self.tokens[b1]:
                for a in self.tokens[b1][b2]:
                    a1, a2, a3 = a.fingerprint
                    if a3 == b3:
                       matches.append((a, b)) 

        ''' Sort all found matches based on original file. '''
        file_matches = sort_per_filename(matches)
        del matches

        ''' Check each possible file match. If the candidate has a match for at
            least 50% of the input tokens around the same time interval, it
            is very likely the correct match. '''
            
        best_match = None
        
        threshold_coverage = 0.4 * len(tokens)
        threshold_concentration = 0.2
            
        for filename, fmatches in file_matches.iteritems():
            
            if len(fmatches) < threshold_coverage:
                continue
            
            dt = [match[0].time - match[1].time for match in fmatches]
            upper_bound = np.ceil(np.max(dt))
            lower_bound = np.floor(np.min(dt))
             
            """ Create a histogram with binsize 1. The two additional bins at 
                the edges are to make sure the next step always goes well. """
            binsize = 0.1
            histogram, bins = np.histogram(dt, bins=np.arange(lower_bound - binsize, upper_bound + 3 * binsize, binsize))

            maxindex = np.argmax(histogram)
            coverage = np.sum(histogram[maxindex-1:maxindex+1])
            concentration = float(coverage) / len(fmatches)
            
            #if filename == "training/pokemon/441.wav":
            #    print coverage, concentration
                
            #if filename == "training/pokemon/441.wav":
            """width = 0.7 * (bins[1] - bins[0])
            center = (bins[:-1] + bins[1:]) / 2
            plt.bar(center, histogram, align='center', width=width)
            ax = plt.gca()
            ax.set_title(filename)
            plt.show()"""
            
            if coverage > threshold_coverage and concentration > threshold_concentration and (best_match is None or coverage > best_match[1]):
                best_match = (filename, coverage)
                    
        if best_match is not None:
            return best_match[0]
        return None
