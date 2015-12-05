from soundfiles import *
from fingerprint import *
from classifier import *
import sys

if __name__ == "__main__":

    tutorial = "use: main.py [database] [signal]"

    """try:
        database = database.load(arg[1])
    except:
        print "something went wrong with loading the database\n", tutorial
        sys.exit()

    try:
        signal = soundfiles.load_signal("audio/" + arg[2])
        if signal == None:
            raise
    except:
        print "something went wrong with loading the signal\n", tutorial
        sys.exit()"""

    cl = Classifier()

    database_files = [("training/track01_ijsvogel.wav", "Ijsvogel"), ("training/track03_goudvink.wav", "Goudvink")]
    for filepath, bird in database_files:
        print "Adding file %s to database" % filepath
        signal = load_wav(filepath)
        tokens = get_tokens(signal, 1024, 1, bird)
        for token in tokens:
            cl.add_token(token)
    
    print "Recognizing input file"
    signal = load_wav("audio/goudvink.wav")
    tokens = get_tokens(signal, 1024, 1, "Zoek")
    print "It's a %s!" % cl.classify(tokens)

    # fingerprint.get_fingerprints(signal)

    # create classifier from database

    # get input file fingerprints

    # match fingerprints using the classifier

    # print output
