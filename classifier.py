'''
The classifier uses a hashtable based on fingerprint hashes.
For each possible matched file, check whether the time points between the
hashes are more or less the same.
'''


class Token:
    '''
    '''
    def __init__(self, fingerprint, time, filename):
        self.fingerprint = fingerprint
        self.time = time
        self.filename = filename


class Classifier:
    '''
    '''
    def __init__(self):
        pass

    def add_token(self, token):
        pass

    def classify(self, fingerprints):
        pass
