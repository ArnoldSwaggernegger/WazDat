"""
    main.py

"""

from sys import argv, exit

from soundfiles import load_signal
from database import Database
from fingerprint import get_tokens

if __name__ == "__main__":

    if len(argv) < 3:
        print "usage: main.py [database] [signal]"
        exit()

    database_name = argv[1]
    database = Database(database_name)
    
    if database is None:
        print "This database could not be loaded"
        exit()

    filename = argv[2]
    print "Reading %s" % filename
    signal = load_signal(filename)
    
    if signal is None:
        print "This audio file could not be loaded"
        exit()

    tokens = get_tokens(signal)
    classifier = database.as_classifier()

    print "Classifying..."
    match = classifier.classify(tokens)
    
    if match:
        print "File {} matches with database entry {}".format(filename, match)
    else:
        print "File {} could not be matched".format(filename)
