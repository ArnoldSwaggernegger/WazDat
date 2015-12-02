class Token:

    def __init__(self, fingerprint, time, filename):
        self.fingerprint = fingerprint
        self.time = time
        self.filename = filename
        

""" The classifier uses a hashtable based on fingerprint hashes. The filename 
    and time point are used to match the song using multiple similar hashes. 
"""

class Classifier:

    def __init__(self):
        pass
        
    def add_token(self, token):
        pass
        
    def classify(self, fingerprints):
        pass
