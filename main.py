'''
main.py
'''

import argparse
from database import Database
from soundfiles import load_signal
from sys import exit
from fingerprint import get_tokens

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Classify audio.')
    parser.add_argument(
        'database', metavar='database', type=str,
        help='Database to use.'
    )
    parser.add_argument(
        'signal', metavar='signal', type=str,
        help='Signal to classify'
    )

    args = parser.parse_args()

    database = Database(args.database)
    if database is None:
        print 'This database could not be loaded'
        parser.print_help()
        exit()

    signal = load_signal(args.signal)
    if signal is None:
        print 'This audio file could not be loaded'
        parser.print_help()
        exit()

    print 'Analyzing {}...'.format(signal.get_filename())
    tokens = get_tokens(signal)

    print 'Reading database \'{}\'...'.format(str(database))
    classifier = database.as_classifier()

    print "Classifying..."
    match = classifier.classify(tokens)

    if match:
        print "File {} matches with database entry {}".format(
            signal.filename, match
        )
    else:
        print "File {} could not be matched".format(signal.filename)
